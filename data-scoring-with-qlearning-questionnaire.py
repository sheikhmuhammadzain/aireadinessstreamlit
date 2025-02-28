import numpy as np

# ✅ Hardcoded Questionnaire (Categorized)
questionnaire = {
    "Data Accessibility & Cataloging": [
        "Is your data catalogued for easy access by AI teams?",
        "Do you maintain data dictionaries to standardize metadata?",
        "How frequent is your data updated for AI use cases?",
        "Do you support multi-modal data integration for AI?",
    ],
    "Data Governance & Compliance": [
        "Is your data governance aligned with AI requirements?",
        "How secure is your external data ingestion process?",
        "Do you audit external data sources for quality and reliability?",
        "Do you use version control for data sets used in AI?",
        "How comprehensive is your data anonymization process?",
        "Do you conduct regular data lineage audits?",
    ],
    "Data Quality & Processing": [
        "Do you have automated data cleansing pipelines?",
        "Are labeling processes standardized for supervised learning?",
        "How prepared are your data formats for new AI applications?",
        "Do you assess the energy consumption of data processing?",
        "Are duplicate records identified and removed from the dataset?",
        "What mechanisms do you use to detect and manage outliers in structured datasets?",
    ],
    "Bias & Fairness in AI Data": [
        "Do you have tools to identify biases in data pipelines?",
        "How is the data checked for biases (e.g., gender, race, class imbalance)?",
        "Do you use tools to calculate fairness metrics, such as the Gini-Simpson Index or P-Difference metrics?",
        "Are mechanisms like synthetic data generation used, and how is closeness to real data evaluated?",
        "Is your data aligned with FAIR principles (Findable, Accessible, Interoperable, Reusable)?",
    ],
    "Data Infrastructure & Security": [
        "Do you have internal tools for synthetic data generation?",
        "Is your data pipeline automated for repeatable experiments?",
        "Do you use cloud-native data tools for AI processing?",
        "Are there contingency plans for data breaches in AI systems?",
        "How do you ensure that datasets used for training are current and relevant?",
        "Are advanced ETL workflows and data lakes in place to centralize fragmented datasets?",
    ],
}

# ✅ Dictionary to store responses
user_responses = {category: [] for category in questionnaire.keys()}

# ✅ Asking Questions
for category, questions in questionnaire.items():
    print(f"\n🔹 **Category: {category}**")
    for question in questions:
        while True:
            try:
                response = int(
                    input(f"{question}\nEnter your response (1-4, where 1 = Strongly Disagree, 4 = Strongly Agree): "))

                if response < 1 or response > 4:
                    print("⚠️ Invalid input. Please enter a number between 1 and 4.")
                    continue

                user_responses[category].append(response)
                break
            except ValueError:
                print("⚠️ Invalid input. Please enter a valid number (1-4).")

# ✅ Compute Category Scores
category_scores = {category: np.mean(scores) for category, scores in user_responses.items()}

# ✅ Initialize Q-values (Reinforcement Learning)
q_values = {category: np.random.uniform(0, 1) for category in questionnaire.keys()}

# ✅ Reinforcement Learning Parameters
alpha = 0.1  # Learning rate
gamma = 0.9  # Discount factor
reward = 1  # Assume a reward of 1 for simplicity

# ✅ Updating Q-values iteratively based on reinforcement learning
for _ in range(10):  # Simulate multiple learning iterations
    for category in questionnaire.keys():
        q_values[category] = q_values[category] + alpha * (reward + gamma * max(q_values.values()) - q_values[category])

# ✅ Compute Softmax Weights **AFTER UPDATING Q-values**
eta = 1.0  # Softmax scaling parameter
exp_q_values = np.exp(eta * np.array(list(q_values.values())))
softmax_weights = exp_q_values / np.sum(exp_q_values)

# ✅ Compute Final AI Data Readiness Score (Weighted Sum)
overall_score = sum(category_scores[cat] * softmax_weights[i] for i, cat in enumerate(questionnaire.keys()))

# ✅ Display Results
print("\n🏆 **AI Data Readiness Scores:**")
for category in questionnaire.keys():
    print(f"{category}: {category_scores[category]:.2f}")

# ✅ Display Updated Q-values
print("\n🔹 **Updated Q-values after Learning:**")
for category, q_val in q_values.items():
    print(f"{category}: {q_val:.3f}")

# ✅ Display Softmax Weights
print("\n🔹 **Updated Softmax Weights:**")
for category, weight in zip(questionnaire.keys(), softmax_weights):
    print(f"{category}: {weight:.3f}")

print("\n🔹 **Final AI Data Readiness Score:**", round(overall_score, 2))
