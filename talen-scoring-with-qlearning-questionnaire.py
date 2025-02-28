import numpy as np

# ✅ Hardcoded Questionnaire (Categorized)
questionnaire = {
    "AI Talent Acquisition": [
        "Do you have a structured AI hiring strategy?",
        "Are your hiring policies tailored for AI-specific skills?",
        "Do you recruit globally for AI talent?",
        "Are your job roles for AI well-defined?",
    ],
    "AI Upskilling & Training": [
        "Are employees receiving AI training and certifications?",
        "Do you conduct regular AI capability assessments for your staff?",
        "Are staff incentivized for AI upskilling?",
        "Is there a mentorship program for junior AI staff?",
    ],
    "AI Cross-Functional Collaboration": [
        "Are AI initiatives aligned across different business units?",
        "Do you partner with universities for AI research?",
        "Do you encourage interdisciplinary collaboration in AI projects?"
    ],
    "AI Leadership & Culture": [
        "Are leaders AI-literate and promoting AI adoption?",
        "Do you track the career growth of your AI team?"
    ],
    "MLOps & AI Engineering": [
        "Are AI engineering best practices (MLOps, CI/CD) being followed?",
        "Do you have monitoring systems in place for AI models?",
        "How frequently do you retrain AI models to maintain performance?"
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
print("\n🏆 **AI Talent Readiness Scores:**")
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

print("\n🔹 **Final AI Talent Readiness Score:**", round(overall_score, 2))
