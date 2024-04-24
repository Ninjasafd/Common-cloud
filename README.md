# Common Cloud Use

## Description
Common Cloud is a centralized Python library that gives a developer access to cloud services from different providers. It does this by making use of cloud service APIs, software interfaces that allow a user to communicate with a service by sending and requesting data. 
Usually, each API call is unique because of different required inputs or "fields". However, Common Cloud solves this by standardizing all inputs and outputs behind the scenes using data structures and software design patterns, simplifying the process for users. A user only needs to send a request for a specific service and provider via a function call. Then, Common Cloud will process the inputs and format them into a specific form for a service API. The formatted data is then sent to the API, which processes the given information and responds with the desired data. Lastly, the desired data is processed by Common Cloud and returned in a standard form.

## Software Required
This test script requires Python and a few packages to run. The below line is required.

```pip install python-dotenv```

These are all the packages required for providers. The factory may not work properly if all of the below packages aren't installed.

Service Provider | Python Package Necessary
------------- | -------------
Clarifai  | `clarifai-grpc `
DetectLanguage | `detectlanguage`
Deepgram | `deepgram-sdk`, also require Microsoft Visual C++ 14.0 or greater
Google Language Detection | `google-cloud-language`
Google Cloud Speech Services| `google-cloud-speech`
Google Other | `google-cloud-translate`
Lettria | `lettria==5.5.2`
Microsoft Speech Services | `azure-cognitiveservices-speech`
Microsoft Other | `azure-ai-textanalytics`

Google API Key - `https://console.cloud.google.com/apis/credentials`


## Using the software
This section explains how to use the different services. The easiest way is to use the service files in the `cloud` subfolder. First, let's change folders or directories into the cloud folder.

```cd .\common-cloud\cloud\```

From here, we can access `sentiment.py`, `language_detector.py`, and other service files, which we can use to perform API calls.


Let's run through an example with `language_detector.py`, which can be accessed in two ways. The first is to directly call the file with inputs in a terminal in the form `py language_dector.py {provider_name} {text}`. For example:

```py language_detector.py "Google" "This is definitely English."```

produces

`{'language': 'en', 'confidence': 1.0}`

The second way is demonstrated at the bottom of the file. This method is most useful when calling the service from a different file like when testing a dataset. 
``` 
1   text = "This is a phrase to be detected"
2
3   for service in language_detect_services:
4       model = Language(service, keys)
5       y = model(text)
6       print(service, ": ", y)
```
In this case, line 4 returns a Language Detection model from the respective factory class. This is done in the `Language` class call. From there, you can call the model using parameters, like in line 5 with `model(text)`. The standardized response is then stored in y, which can be manipulated, such as being printed.



# Inputs and Outputs

An example of the model call and response is shown below.
```
model = Service_Factory_Name(service, keys)
y = model({set of inputs})
```
A table of the set of inputs is shown below:
Service Type | Standardized Input Format
------------- | -------------
`Speech-To-Text`  | (speech_file_name)
`Translate Languages` | (text, source_language, target_language)
`Language Detection` | (text)
`Sentiment Analysis` | (text)
`Text-to-Speech` | (text)

A table of standardized outputs is shown below:
Service Type | Standardized Output Format
------------- | -------------
`Speech-To-Text`  | { "confidence" : [0 - 1], text : [text]}
`Translate Languages` | { "confidence" : [0 - 1], "output": [translated text],"source_language": [source language],"target_language": [target language]}
`Language Detection` | {"language" : [language code], "confidence : [value]}
`Sentiment Analysis` | {"score" : [value], "type" [positive, negative, neutral]} or {"positive" : [score], "neutral" : [score], "negative" : [score]}
`Text-to-Speech` | .wav file


### Link to spreadsheet
https://docs.google.com/spreadsheets/d/1s3HqEX7XlvFKPFv-vqmBvmiINvF62LicjLNUlc_4uMc/edit#gid=0
