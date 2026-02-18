# Health Care Assistant

This project is a **Health Care Assistant** application built using Python, [LangChain](https://langchain.com/), and [Streamlit](https://streamlit.io/). It leverages OpenAI's language model to analyze symptoms, suggest possible conditions, recommend first aid medications, and provide nutritional food suggestions.

## Features

- **Symptom Analysis**: Identifies two possible conditions based on user-provided symptoms.
- **First Aid Medications**: Suggests two first aid medications for the identified conditions.
- **Nutritional Recommendations**: Recommends two nutritional foods for the identified conditions.
- **Memory Management**: Maintains conversation history for symptoms, medications, and nutrition.

## How It Works

1. **Input Symptoms**: Users enter their symptoms or health concerns into a text input field.
2. **Sequential Processing**:
    - The app analyzes symptoms to identify possible conditions.
    - It suggests first aid medications for the identified conditions.
    - It recommends nutritional foods for the conditions.
3. **Results Display**: The app displays the results in a structured format, along with expandable sections for detailed memory history.

## Technologies Used

- **LangChain**: For building and managing the chains of prompts and memory.
- **OpenAI**: For natural language processing and generating responses.
- **Streamlit**: For creating the user interface.
- **Python**: Core programming language.


## File Structure

- `main.py`: Contains the main application logic.
- `constants.py`: Stores the OpenAI API key.
- `requirements.txt`: Lists the required Python packages.

## Future Enhancements

- Add support for more detailed medical advice.
- Integrate with external APIs for real-time health data.
- Improve the user interface for better accessibility.


