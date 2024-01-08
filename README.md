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

# Using the App with Dataset

- If are using a test dataset, place the dataset csv file at the root folder of the project
- Run `python3 data_extraction_script.py` to extract information using GPT-4 API and move it to the `outputs/` folder. There is already a extracted dataset called `outputs/combined_data_first_200_rows.jsonl` for the training dataset. 