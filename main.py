import torch
from torch.utils.data import TensorDataset, DataLoader, RandomSampler
# , SequentialSampler
# import torch.nn.functional as F
from sklearn.model_selection import train_test_split
# from transformers import BertConfig, BertModel
from transformers import BertTokenizer, AdamW
from transformers import BertForSequenceClassification
from transformers import get_linear_schedule_with_warmup
# from tqdm import tqdm, trange, tqdm_notebook
from tqdm import tnrange
import pandas as pd
# import io
import numpy as np
# Import and evaluate each test batch using Matthew's correlation coefficient
# from sklearn.metrics import accuracy_score, matthews_corrcoef
import random
# import os

# identify and specify the GPU as the device,
# later in training loop we will load data into device
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
device = torch.device("cpu")
# n_gpu = torch.cuda.device_count()
# torch.cuda.get_device_name(0)

SEED = 19

random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)
if device == torch.device("cuda"):
    torch.cuda.manual_seed_all(SEED)

# print(device, n_gpu, torch.cuda.get_device_name(0))

# Reading Data into dataFrame
# BERT-big5/big5/myPersonalitySmallReal - per hpc status and labels
text = pd.read_csv(
        "~/Venv/Documents/dataset/myPersonalitySmall/statuses_unicode.txt",
        header=None,
        names=['sentence'])
big5 = pd.read_csv(
        "../dataset/myPersonalitySmall/big5labels.txt",
        delimiter=" ",
        header=None,
        names=['O', 'C', 'E', 'A', 'N'])
# print(text.sample(5))
# print(text.sentence.size)

df = pd.concat([text, big5], axis=1, sort=False)
print(df.sample(5))
# df = df.iloc[0:4]
max_len = 0
for i in df['sentence']:
    # print(len(str(i)))
    if (len(str(i)) > max_len):
        max_len = len(str(i))
print(max_len)

MAX_LEN = 512  # the nearest power of 2
# Import BERT tokenizer, that is used to convert our text into
# tokens that corresponds to BERT library
tokenizer = BertTokenizer.from_pretrained(
                'bert-base-multilingual-cased',
                do_lower_case=False)

df['sentence'] = df['sentence'].astype('str')
# from object to string (sometimes str sometimes string)
sentences = df.sentence.values
# print(sentences)
input_ids = [tokenizer.encode(sent,
                              add_special_tokens=True,
                              max_length=MAX_LEN,
                              pad_to_max_length=True) for sent in sentences]

# print("Actual sentence before tokenization: ",sentences[2])
# print("Encoded Input from dataset: ",input_ids[2])

# Create attention mask
attention_masks = []
# Create a mask of 1 for all input tokens and 0 for all padding tokens
attention_masks = [[float(i > 0) for i in seq] for seq in input_ids]
# print(attention_masks[2])

labels = df.O.values  # wroking with OPENNESS !!!

train_inputs, validation_inputs, train_labels, validation_labels = \
    train_test_split(input_ids, labels, random_state=SEED, test_size=0.1)
train_masks, validation_masks, _, _ =   \
    train_test_split(attention_masks,
                     input_ids,
                     random_state=SEED,
                     test_size=0.1)

# convert all our data into torch tensors, required data type for our model
train_inputs = torch.tensor(train_inputs)
validation_inputs = torch.tensor(validation_inputs)
train_labels = torch.tensor(train_labels).float()
validation_labels = torch.tensor(validation_labels).float()
train_masks = torch.tensor(train_masks)
validation_masks = torch.tensor(validation_masks)

# Select a batch size for training. For fine-tuning BERT on a specific task,
# the authors recommend a batch size of 16 or 32
batch_size = 4

# Create an iterator of our data with torch DataLoader. This helps save on
# memory during training because, unlike a for loop,
# with an iterator the entire dataset does not need to be loaded into memory
train_data = TensorDataset(train_inputs, train_masks, train_labels)
train_sampler = RandomSampler(train_data)
train_dataloader = DataLoader(train_data, sampler=train_sampler,
                              batch_size=batch_size)

validation_data = TensorDataset(validation_inputs,
                                validation_masks,
                                validation_labels)
validation_sampler = RandomSampler(validation_data)
validation_dataloader = DataLoader(validation_data,
                                   sampler=validation_sampler,
                                   batch_size=batch_size)

# Load BertForSequenceClassification, the pretrained BERT model
# with a single linear classification layer on top.
model = BertForSequenceClassification.from_pretrained(
            "bert-base-multilingual-cased",
            num_labels=1).to(device)
# setting num_label=1 configure the model to perform regression
# and change the loss into Mean-Square Loss

# Parameters:
lr = 2e-5
adam_epsilon = 1e-8

# Number of training epochs (authors recommend between 2 and 4)
epochs = 3

num_warmup_steps = 0
num_training_steps = len(train_dataloader)*epochs

# Prepare optimizer and schedule (linear warmup and decay)
# no_decay = ['bias', 'LayerNorm.weight']
# optimizer_grouped_parameters = [
#     {'params': [p for n, p in model.named_parameters()
#       if not any(nd in n for nd in no_decay)], 'weight_decay': 0.01},
#     {'params': [p for n, p in model.named_parameters()
#       if any(nd in n for nd in no_decay)], 'weight_decay': 0.0}
#     ]

# In Transformers, optimizer and schedules are splitted and
#  instantiated like this:
# optimizer = AdamW(optimizer_grouped_parameters, lr=lr, eps=adam_epsilon)
optimizer = AdamW(model.parameters(),
                  lr=lr,
                  eps=adam_epsilon,
                  correct_bias=False)
# To reproduce BertAdam specific behavior set correct_bias=False
scheduler = get_linear_schedule_with_warmup(
                optimizer,
                num_warmup_steps=num_warmup_steps,
                num_training_steps=num_training_steps)
# PyTorch scheduler

# Store our loss and accuracy for plotting
train_loss_set = []
learning_rate = []

# Gradients gets accumulated by default
model.zero_grad()

# tnrange is a tqdm wrapper around the normal python range
for _ in tnrange(1, epochs+1, desc='Epoch'):
    print("<" + "="*22 + F" Epoch {_} " + "="*22 + ">")
    # Calculate total loss for this epoch
    batch_loss = 0

    for step, batch in enumerate(train_dataloader):
        # Set our model to training mode (as opposed to evaluation mode)
        model.train()
        # Add batch to GPU
        batch = tuple(t.to(device) for t in batch)
        # Unpack the inputs from our dataloader
        b_input_ids, b_input_mask, b_labels = batch

        # Forward pass
        outputs = model(b_input_ids,
                        token_type_ids=None,
                        attention_mask=b_input_mask,
                        labels=b_labels)
        loss = outputs[0]

        # Backward pass
        loss.backward()

        # Clip the norm of the gradients to 1.0
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        # Gradient clipping is not in AdamW anymore
        # (so you can use amp without issue)

        # Update parameters and take a step using the computed gradient
        optimizer.step()

        # Update learning rate schedule
        scheduler.step()

        # Clear the previous accumulated gradients
        optimizer.zero_grad()

        # Update tracking variables
        batch_loss += loss.item()

    # Calculate the average loss over the training data.
    avg_train_loss = batch_loss / len(train_dataloader)

    # store the current learning rate
    for param_group in optimizer.param_groups:
        print("\n\tCurrent Learning rate: ", param_group['lr'])
        learning_rate.append(param_group['lr'])

    train_loss_set.append(avg_train_loss)
    print(F'\n\tAverage Training loss: {avg_train_loss}')

    # Validation

    # Put model in evaluation mode to evaluate loss on the validation set
    model.eval()

    # Tracking variables
    nb_eval_steps = 0

    # Evaluate data for one epoch
    for batch in validation_dataloader:
        # Add batch to GPU
        batch = tuple(t.to(device) for t in batch)
        # Unpack the inputs from our dataloader
        b_input_ids, b_input_mask, b_labels = batch
        # Telling the model not to compute or store gradients,
        # saving memory and speeding up validation
        with torch.no_grad():
            # Forward pass, calculate logit predictions
            logits = model(b_input_ids,
                           token_type_ids=None,
                           attention_mask=b_input_mask)
            print("logits", logits)

        # Move logits and labels to CPU
        logits = logits[0].to('cpu').numpy()
        # in this case logits represent the predicted value
        # for the regression on a float number
        label_ids = b_labels.to('cpu').numpy()

        # print(logits, label_ids)
        # pred_flat = np.argmax(logits, axis=1).flatten()
        # labels_flat = label_ids.flatten()
        # tmp_eval_accuracy = accuracy_score(pred_flat, labels_flat)
        # tmp_eval_mcc_accuracy = matthews_corrcoef(labels_flat, pred_flat)

        # eval_accuracy += tmp_eval_accuracy
        # eval_mcc_accuracy += tmp_eval_mcc_accuracy
        # nb_eval_steps += 1

    # print(F'\n\tValidation Accuracy: {eval_accuracy/nb_eval_steps}')
    # print(F'\n\tValidation MCC Accuracy: {eval_mcc_accuracy/nb_eval_steps}')

path_model = "model/"
path_tokenizer = "tokenizer/"
model.save_pretrained(path_model)
tokenizer.save_pretrained(path_tokenizer)
model_save_name = 'fineTuneModel.pt'
path_model = path_model+model_save_name
torch.save(model.state_dict(), path_model)
