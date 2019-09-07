## 1.Introduction

![Image description](workflow.png)
*Fig. 1: Overall workflow of our method*

In this project we use stylegan to create audio reactive visuals for VJ. Given an audio clip we first perform feature extraction using FFT and filtering to separate different sounds such as bass and snare. Then for every time-step we calculate the magnitude of changes in these features and map them to movement in the latent space of stylegan (walking in latent space). The latent vectors obtained after this step is joined by style mixing to create an image for every time-step. (See original stylegan [paper](https://arxiv.org/abs/1812.04948) for details on style mixing) Concatenating the images and we obtain a video clip that "dances" to the audio clip. The overall workflow is shown in Fig. 1.

## 2.Expermiments

### 2-1.Hand Crafted Features
<iframe width="256" height="256"
src="https://www.youtube.com/embed/D6UG09FOSqw">
</iframe>
<iframe width="256" height="256"
src="https://www.youtube.com/embed/Vxvgc8muBXw">
</iframe>

In this experiment we first perform FFT and filtering on the audio clip then calculate the changes in the features for every time-step and map to stylegan according to Fig. 2. Random walk is used to move in latent space by generating a random direction vector for every time-step and multiplying by the magnitude of the change. The max walk length limits the maximum distance the latent vector can move in one time-step.

| Filter Type   | Frequencies   | Sounds               | Styles (layers) | Effect           | Max Length |
| ------------- |:-------------:|:--------------------:|:---------------:|:----------------:|:----------:|
| Low Pass      | ~150 Hz       | Bass                 | 0~2             | Coarse Structure | 4 vs 10    |
| High Pass     | 500~5000 Hz   | Mid-High Frequencies | 3~5             | Mid Level        | 4 vs 10    |
| Band Pass     | 200~350 Hz    | Snare                | 6~13            | Fine Detail      | 3 vs 3     |

*Fig. 2: Filter settings and mapping to stylegan*

#### Ablation
<iframe width="256" height="256"
src="https://www.youtube.com/embed/lVszLh0iUs4">
</iframe>
<iframe width="256" height="256"
src="https://www.youtube.com/embed/wR-pnOy8R9k">
</iframe>
<iframe width="256" height="256"
src="https://www.youtube.com/embed/07A5MKOW7y4">
</iframe>

Here we perform some ablation experiments by fixing the style vectors from two of the filters and varying only one. The videos are results for low pass, band pass and high pass respectively.

### 2-2.Nsynth Extracted Features

### 2-3.Learned Walks

## 3.Resources

Paper: Coming Soon

Code: Coming Soon

### Markdown

Markdown is a lightweight and easy-to-use syntax for styling your writing. It includes conventions for

```markdown
Syntax highlighted code block

# Header 1
## Header 2
### Header 3

- Bulleted
- List

1. Numbered
2. List

**Bold** and _Italic_ and `Code` text

[Link](url) and ![Image](src)
```

For more details see [GitHub Flavored Markdown](https://guides.github.com/features/mastering-markdown/).

### Jekyll Themes

Your Pages site will use the layout and styles from the Jekyll theme you have selected in your [repository settings](https://github.com/hanhung/DeepVJ/settings). The name of this theme is saved in the Jekyll `_config.yml` configuration file.

### Support or Contact

Having trouble with Pages? Check out our [documentation](https://help.github.com/categories/github-pages-basics/) or [contact support](https://github.com/contact) and we’ll help you sort it out.
