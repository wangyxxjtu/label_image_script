# Label the images

Requirements:
 * python 3.6
 * PyQt5
 * requests
 * skimage

Install python 3.6 and pip, and install the requirements:
``` bash
pip install python-qt5 requests scikit-image #for windows/mac 
pip install --user pyqt5 requests scikit-image #for ubuntu 
```

Then, run the main.py to start:
``` bash
python main.py
```
Steps:
* Download this project and install the requirements.
* Select or input the beginning image ID in the top "Image ID" box.
* Input the key words (split by newline character)for two images in their corresponding text areas or select the check boxes.
* Click 'Next Sample' to continue, and the result will be automatically saved in './caption_result/' dir.
 
Relus to follow：
* Key words mainly depends on your subjective judgement, the candidates in check boxes are only for reference purpose.
* If you think the candidate labels in check boxes match the image content, just tick it.
* As for the key words matching the image but missed in check boxes, you should manually type them.
* Each image should have 3-5 labels

Example

![image](example.png)

The program may be stuck when you press the button, this is caused by the remote image requesting, please wait a moment ...

The "Category" and "Attribution" show some classification information and attributions, they are predicted by the [Place365 model](https://github.com/CSAILVision/places365) and are only for reference purpose, because they are not reliable enough.

When your work finished, pack the './caption_result/' to file 'start-id_end-id.zip', e.g. '10_100.zip', and upload it in [this site](http://holer.cc:50347)
# Thank you very much!
