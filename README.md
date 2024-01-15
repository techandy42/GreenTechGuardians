# GreenTechGuardians

A Circular Economy business idea evaluator tool built using Gen-AI.

# Set-up

- Clone the repository: `git clone https://github.com/techandy42/GreenTechGuardians.git`
- Naivagate into the repository: `cd GreenTechGuardians`
- Set-up virtual environment: `python3 -m venv env` (Mac/Linux) or `python -m venv env` (Windows)
- Activate the virtual environment: `source env/bin/activate` (Mac/Linux) or `.\env\Scripts\activate` (Windows)
- Install packages: `pip install -r requirements.txt`
- Create `.env` file in the root folder of the project
- Add `OPENAI_API_KEY=` environment variable with your OpenAI API Key
- Add `PINECONE_API_KEY=` environment variable with your Pinecone API Key

# To run the final application
- To just run the final application, please ask us for the Pinecone API Key
- In the terminal, run `streamlit run app.py`

# Using the App with Dataset

- If are using a test dataset, place the dataset csv file at the root folder of the project
- Run `python3 data_extraction_script.py` to extract information using GPT-4 API and move it to the `outputs/` folder. There is already a extracted dataset called `outputs/extracted_data_training_dataset.jsonl` for the training dataset. Rename the target dataset name in the code as needed.
- Run `python3 semantic_search/create_search_engine.py` to create an index in Pinecone. Change the name of the source extracted jsonl file as needed.
- Run `streamlit run app.py`. Rename the jsonl file name as needed. Make sure you name the Pinecone index in `app.py` as same as your actual Pinecone index.
- If you run into additional problems, please feel free to contact us.

# Contact Info

- Andy Lee: techandy42@gmail.com
- Malinda Lu: malindalu0611@gmail.com 
- Serena Pei: serenapei123@gmail.com 
- Yongan Yu: yya040327@gmail.com
