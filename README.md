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
- Install package: `pip install streamlit`
- In the terminal, run `streamlit run app.py`

# To run data collection on a new dataset
- Go to `data_extraction_script.py`, set df to read from new file
- Go to `combine_data_script.py`, set original_dataset to read from new file
 
