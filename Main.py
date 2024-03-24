import streamlit as st
from translate import Translator

# OPENAI API -------------- GPT - LLM
from openai import OpenAI
API_KEY = "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"
client = OpenAI(
    api_key=API_KEY,
)

def get_chatgpt_response(input):
    completion = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "system", "content": """You are a helpful assistant which give the prompt for state of art ai diffuser models.Please only give output in english language. 
                """},
        {"role": "user", "content": input}
      ]
    )
    print(completion)
    print("-------------------")
    print(completion.choices[0].message.content)
    return completion.choices[0].message.content
#---------------------------------------------------------------------------------

#----------------------------- Image generation ----------------------------------

PAT = 'dafa11fd7e7949e7ab8054011c4c9011'
USER_ID = 'stability-ai'
APP_ID = 'stable-diffusion-2'
MODEL_ID = 'stable-diffusion-xl'
MODEL_VERSION_ID = '68eeab068a5e4488a685fc67bc7ba71e'
USER_ID_2 = 'clarifai'
APP_ID_2 = 'main'
MODEL_ID_2 = 'general-image-recognition'
MODEL_VERSION_ID_2 = 'aa7f35c01e0642fda5cf400f543e7c40'

from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2

def generate_image(prompt):

    channel = ClarifaiChannel.get_grpc_channel()
    stub = service_pb2_grpc.V2Stub(channel)

    metadata = (('authorization', 'Key ' + PAT),)

    userDataObject = resources_pb2.UserAppIDSet(user_id=USER_ID, app_id=APP_ID)

    post_model_outputs_response = stub.PostModelOutputs(
        service_pb2.PostModelOutputsRequest(
            user_app_id=userDataObject,
            model_id=MODEL_ID,
            version_id=MODEL_VERSION_ID,
            inputs=[
                resources_pb2.Input(
                    data=resources_pb2.Data(
                        text=resources_pb2.Text(
                            raw=prompt
                        )
                    )
                )
            ]
        ),
        metadata=metadata
    )
    if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
        print(post_model_outputs_response.status)
        raise Exception("Post model outputs failed, status: " + post_model_outputs_response.status.description)

    output = post_model_outputs_response.outputs[0]

    base64_image = output.data.image.base64
    image_filename = f"Output_image.jpg"
    with open(image_filename, 'wb') as f:
        f.write(base64_image)

    print("Generated successfully")
    st.image(base64_image)

#------------------------- Translation ------------------------------

def trans(statement):
    translator = Translator(to_lang = 'en')
    translation = translator.translate(statement)
    return translation


#------------------------- streamlit page ---------------------------
st.title("Welcome to Multilingual Text to image Generator Chatbot!")
text = st.text_input("Craft a message to generate an image with your text")

if (st.button('Send')):
    inp = trans(text)
    st.write(inp)
    prompt = get_chatgpt_response(inp)
    print("PROMPT", prompt)
    st.write(prompt)
    generate_image(prompt)
    st.success("GENERATED")
