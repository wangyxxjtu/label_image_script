# label_image_script
The script to label image with a sentence

Requirements:
 * python 3.6
 * PyQt5
 * requests
 * json

Install python 3.6 and pip, then
``` bash
pip install python-qt5 requests json
```

Then, run the main.py to annotate image
``` bash
python main.py
```
Example

![image](example.png)

Steps:
* select or input the image Id in the top "Image ID" box.
* input the descriptions for two image.
* Click next to continue.

The "Category" and "Attribution" shows some classification information and attributions, they are predicted by the [Place355 model](https://github.com/CSAILVision/places365) and are only for reference purpose, because they are not reliable.

# Thank you very much!
