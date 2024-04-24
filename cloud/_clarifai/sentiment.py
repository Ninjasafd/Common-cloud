import sys
import json
from pprint import pprint

# Mocking
import os
from dotenv import load_dotenv
load_dotenv()
MOCKING_TEST = os.getenv("MOCKING")

from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import service_pb2_grpc
from clarifai_grpc.grpc.api import service_pb2, resources_pb2
from clarifai_grpc.grpc.api.status import status_code_pb2


class Sentiment:
    def __init__(self, api_key, user_id, app_id, model_id):
        self._stub = service_pb2_grpc.V2Stub(ClarifaiChannel.get_grpc_channel())
        self._metadata = (('authorization', 'Key {}'.format(api_key)),)
        self._userDataObject = resources_pb2.UserAppIDSet(user_id=user_id, app_id=app_id)
        self.model_id = model_id
    def predict(self, text):
        resp = self._stub.PostModelOutputs(
            service_pb2.PostModelOutputsRequest(
                user_app_id=self._userDataObject,
                model_id=self.model_id,
                inputs=[
                    resources_pb2.Input(
                        data=resources_pb2.Data(
                            text=resources_pb2.Text(raw=text)
                        )
                    )
                ]
            ),
            metadata=self._metadata
        )
        concepts = resp.outputs[0].data.concepts
        output = {}
        for concept in concepts:
            output[concept.name] = concept.value

        returnJson = output

        return returnJson
        
    def __call__(self, text):
        if (MOCKING_TEST == 'True'):
            dummyReturn = {'positive': 1, 'neutral': 0, 'negative': 0}
            return dummyReturn
        return self.predict(text)

if __name__ == "__main__":
    text = sys.argv[1]
    with open('keys.json', 'r') as f:
        keys = json.load(f)
    keys = keys['clarifai']
    model = Sentiment(keys['api-key'], keys['user-id'], keys['app-id'], keys['model-id'])
    y = model.predict(text)
    pprint(y)
