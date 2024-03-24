import argparse
import os

import numpy as np
import torch
from tqdm import tqdm
from torch.utils.data import DataLoader
import torch.nn.functional as F
from transformers import AutoConfig, AutoTokenizer
from transformers.optimization import AdamW, get_linear_schedule_with_warmup
from utils import set_seed, collate_fn
from prepro import TACREDProcessor
from evaluation import get_f1, compute_f1, compute_h_f1, accuracy, positive_accuracy, hierarchical_accuracy
from model import REModel
from torch.cuda.amp import GradScaler
from hierarchy_utils import constant

from scorer import score

from transformers import WEIGHTS_NAME
# import wandb

CONFIG_NAME = "config.json"
WEIGHTS_NAME = "pytorch_model.bin"


def evaluate(args, model, features, tag='dev'):
    dataloader = DataLoader(features, batch_size=args.test_batch_size, collate_fn=collate_fn, drop_last=False)
    keys, preds = [], []
    all_probs = []
    for i_b, batch in enumerate(dataloader):
        model.eval()

        inputs = {'input_ids': batch[0].to(args.device),
                  'attention_mask': batch[1].to(args.device),
                  'ss': batch[3].to(args.device),
                  'os': batch[4].to(args.device),
                  }
        keys += batch[2].tolist()
        with torch.no_grad():
            logit = model(**inputs)[0]
            pred = torch.argmax(logit, dim=-1)
            probs = F.softmax(logit, dim=1).data.cpu().numpy().tolist()
        preds += pred.tolist()
        all_probs += np.max(probs, axis=1).tolist()

    keys = np.array(keys, dtype=np.int64)
    preds = np.array(preds, dtype=np.int64)
    p, r, max_f1 = get_f1(keys, preds)
    if args.eval_test:
        print(tag.upper()+" EVALUATION")
        compute_f1(preds, keys)
        compute_h_f1(preds, keys)
        accuracy(preds, keys)
        positive_accuracy(preds, keys)
        hierarchical_accuracy(preds, keys)
        id2label = {val:key for key, val in constant.LABEL_TO_ID.items()}
        labels = [id2label[k] for k in keys]
        predictions = [id2label[p] for p in preds]
        opt ={}
        opt['dataset'] = tag
        opt['model_dir'] = args.output_dir
        opt['out'] = args.output_dir
        opt['prediction-logs'] = args.prediction_logs
        p, r, f1 = score(batch.sentence_ids(), batch.gold(), predictions, all_probs, verbose=True, opt=opt)

    output = {
        tag + "_p": p * 100,
        tag + "_r": r * 100,
        tag + "_f1": max_f1 * 100,
    }
    print(output)
    return max_f1, output


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--data_dir", default="./data/tacred", type=str)
    parser.add_argument("--model_name_or_path", default="roberta-large", type=str)
    parser.add_argument("--input_format", default="typed_entity_marker_punct", type=str,
                        help="in [entity_mask, entity_marker, entity_marker_punct, typed_entity_marker, typed_entity_marker_punct]")

    parser.add_argument("--config_name", default="", type=str,
                        help="Pretrained config name or path if not the same as model_name")
    parser.add_argument("--tokenizer_name", default="", type=str,
                        help="Pretrained tokenizer name or path if not the same as model_name")
    parser.add_argument("--max_seq_length", default=512, type=int,
                        help="The maximum total input sequence length after tokenization. Sequences longer "
                             "than this will be truncated.")

    parser.add_argument("--train_batch_size", default=32, type=int,
                        help="Batch size for training.")
    parser.add_argument("--test_batch_size", default=32, type=int,
                        help="Batch size for testing.")
    parser.add_argument("--learning_rate", default=3e-5, type=float,
                        help="The initial learning rate for Adam.")
    parser.add_argument("--gradient_accumulation_steps", default=2, type=int,
                        help="Number of updates steps to accumulate the gradients for, before performing a backward/update pass.")
    parser.add_argument("--adam_epsilon", default=1e-6, type=float,
                        help="Epsilon for Adam optimizer.")
    parser.add_argument("--max_grad_norm", default=1.0, type=float,
                        help="Max gradient norm.")
    parser.add_argument("--warmup_ratio", default=0.1, type=float,
                        help="Warm up ratio for Adam.")
    parser.add_argument("--num_train_epochs", default=5.0, type=float,
                        help="Total number of training epochs to perform.")
    parser.add_argument("--seed", type=int, default=42,
                        help="random seed for initialization")
    parser.add_argument("--num_class", type=int, default=42)
    parser.add_argument("--evaluation_steps", type=int, default=500,
                        help="Number of steps to evaluate the model")

    parser.add_argument("--dropout_prob", type=float, default=0.1)
    parser.add_argument("--project_name", type=str, default="RE_baseline")
    parser.add_argument("--run_name", type=str, default="tacred")

    parser.add_argument('--filter_out', action='store_true', 
                        help='Remove setences with ambiguous subject entity type from data.')
    parser.add_argument('--relabel', action='store_true', 
                        help='Hierarchical Re-labelling: Mapping finer positive relations to coarser relation from hierarchy.')

    parser.add_argument('--hier_loss', action='store_true',
                        help="Whether to use hierarchical CrossEntropyLoss or normal CrossEntropyLoss")
    parser.add_argument('--lca', action='store_true', 
                        help='True uses lca based distance for hierarchical distance loss, False uses simple distance.')
    parser.add_argument('--hier_normalise', type=float, default=1.0, 
                        help="Normalise Hierarchical Distance loss")
    parser.add_argument('--all_pos', action='store_true', help='Trains a classifier for all positive relations.')

    parser.add_argument("--output_dir", default=None, type=str, required=True,
                        help="The output directory where the model predictions and checkpoints will be written.")
    parser.add_argument("--eval_test", action='store_true',
                        help="For just evaluation on test data")

    #Budget Reannotation
    parser.add_argument('--align_retacred', action='store_true', 
                            help="Fetches Dataset eqivalent to unambiguous retacred")
    parser.add_argument('--budget',type=int, default=0,
                            help='percentage of instances to reannotate')
    parser.add_argument('--prediction_logs', action='store_true', help="Generate prediction logs.")

    args = parser.parse_args()
    # wandb.init(project=args.project_name, name=args.run_name)

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    args.n_gpu = torch.cuda.device_count()
    args.device = device
    if args.seed > 0:
        set_seed(args)

    config = AutoConfig.from_pretrained(
        args.config_name if args.config_name else args.model_name_or_path,
        num_labels=args.num_class,
    )
    config.gradient_checkpointing = True
    tokenizer = AutoTokenizer.from_pretrained(
        args.tokenizer_name if args.tokenizer_name else args.model_name_or_path,
    )

    model = REModel(args, config)
    model.to(0)

    if args.relabel:
        constant.LABEL_TO_ID = constant.RELABELED_LABEL_TO_ID
    if args.all_pos:
        print('Considering only positive labeled sentences..!')
        constant.LABEL_TO_ID.pop('no_relation')
        constant.LABEL_TO_ID = {key:val-1 for key, val in constant.LABEL_TO_ID.items()}

    # train_file = os.path.join(args.data_dir, "train.json")
    # dev_file = os.path.join(args.data_dir, "dev.json")
    test_file = os.path.join(args.data_dir, "test.json")
    # dev_rev_file = os.path.join(args.data_dir, "dev_rev.json")
    # test_rev_file = os.path.join(args.data_dir, "test_rev.json")

    processor = TACREDProcessor(args, tokenizer)
    # train_features = processor.read(train_file, args.filter_out, args.relabel, args.all_pos)
    # dev_features = processor.read(dev_file, args.filter_out, args.relabel, args.all_pos)
    test_features = processor.read(test_file, args.filter_out, args.relabel, args.all_pos)
    # dev_rev_features = processor.read(dev_rev_file, args.filter_out, args.relabel, args.all_pos)
    # test_rev_features = processor.read(test_rev_file, args.filter_out, args.relabel, args.all_pos)

    if len(processor.new_tokens) > 0:
        model.encoder.resize_token_embeddings(len(tokenizer))
    
    model.load_state_dict(torch.load(os.path.join(args.output_dir, WEIGHTS_NAME), map_location="cpu"))
    model.to(args.device)
    evaluate(args, model, test_features, tag="test")


if __name__ == "__main__":
    main()
