import matplotlib
from matplotlib import pyplot as plt
matplotlib.use('agg')
import seaborn as sns 
import io
import base64
from PIL import Image
import numpy as np
import torch
import numpy as np
import matplotlib.pyplot as plt
import torch.nn as nn
from torchvision.transforms.functional import normalize
from torchvision.transforms import transforms


class ConvNet(nn.Module):
    def __init__(self,num_classes=6):
        super(ConvNet,self).__init__()
        self.conv1=nn.Conv2d(in_channels=3,out_channels=12,kernel_size=3,stride=1,padding=1)
        self.bn1=nn.BatchNorm2d(num_features=12)
        self.relu1=nn.ReLU()
        self.pool=nn.MaxPool2d(kernel_size=2)
        self.conv2=nn.Conv2d(in_channels=12,out_channels=20,kernel_size=3,stride=1,padding=1)
        self.relu2=nn.ReLU()
        self.conv3=nn.Conv2d(in_channels=20,out_channels=32,kernel_size=3,stride=1,padding=1)
        self.bn3=nn.BatchNorm2d(num_features=32)
        self.relu3=nn.ReLU()
        self.fc=nn.Linear(in_features=75 * 75 * 32,out_features=num_classes)
        
    def forward(self,input):
        output=self.conv1(input)
        output=self.bn1(output)
        output=self.relu1(output)
        output=self.pool(output)
        output=self.conv2(output)
        output=self.relu2(output)
        output=self.conv3(output)
        output=self.bn3(output)
        output=self.relu3(output)
        output=output.view(-1,32*75*75)
        output=self.fc(output)
        return output

class_names = ['fresh apple', 'fresh banana', 'fresh orange',
                'rotten apple', 'rotten banana', 'rotten orange']
checkpoint=torch.load('best_checkpoint.model')
model=ConvNet(num_classes=6)
model.load_state_dict(checkpoint)
model.eval()

normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                     std=[0.229, 0.224, 0.225])
inv_normalize = transforms.Normalize(
    mean=[-0.485/0.229, -0.456/0.224, -0.406/0.255],
    std=[1/0.229, 1/0.224, 1/0.255]
)
transform = transforms.Compose([
    transforms.Resize((150, 150)),
    transforms.ToTensor(),
    normalize,          
])
#function to convert model outputs into a bar plot
def plot_class_distributions(predictions, class_names, filename='predictions.png'):
    plt.clf()
    ax = sns.barplot(x=class_names, y=predictions)
    ax.set_xlabel("Class names")
    ax.set_ylabel("Confidence")
    ax.set_ylim([0, 1])
    sns.despine(ax=ax, top=True, bottom=True)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(filename)


#function to convert base64 to Image
def convert_to_image(base64_string):
    img_data = base64.b64decode(base64_string)
    buffer = io.BytesIO(img_data)
    img = Image.open(buffer)
    return img



#function to read an image and convert it to base64
def convert_to_string(filename):
    with open(filename, "rb") as image_file:
        data = base64.b64encode(image_file.read())
    return data

import matplotlib
matplotlib.use('Agg')  # switch to a non-interactive backend

def saliency(img, model):
    for param in model.parameters():
        param.requires_grad = False
    
    model.eval()
    
    input = transform(img)
    input.unsqueeze_(0)

    input.requires_grad = True
    preds = model(input)
    score, indices = torch.max(preds, 1)
    score.backward()
    slc, _ = torch.max(torch.abs(input.grad[0]), dim=0)
    slc = (slc - slc.min())/(slc.max()-slc.min())

    # Create a new Figure object
    fig = plt.figure(figsize=(5, 5))

    # Create a new Axes object and plot the saliency map
    ax = fig.add_subplot(111)
    ax.imshow(slc.numpy(), cmap=plt.cm.hot)
    ax.set_xticks([])
    ax.set_yticks([])

    # Save the plot to a file
    fig.savefig('saliency_map.png')

    # Close the Figure object to free memory
    plt.close(fig)