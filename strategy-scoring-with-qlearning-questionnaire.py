import numpy as np

# ✅ Hardcoded Questionnaire (Categorized)
questionnaire = {
    "Data Security & Encryption": [
        "Is training and inference data encrypted and secured?",
        "How robust are your organization's data encryption and protection mechanisms for AI deployments?",
        "Does your organization conduct regular security audits for AI systems?",
        "How does your organization ensure compliance with regulations regarding AI security?"

    ],
    "Model Access Control": [
        "Do you employ explainable AI techniques to enhance transparency?",
        "Are access controls for AI systems well-defined and enforced?",
        "How effectively does your organization monitor unauthorized access to AI systems?",
        "How effectively does your organization manage third-party AI security risks?"
    ],
    "AI API Security": [
        "Are AI model APIs secured against unauthorized calls?",
        "What measures has your organization implemented to secure AI models and datasets?",
        "How frequently does your organization test AI systems for vulnerabilities?",
        "How well does your organization address ethical considerations in AI security?"
    ],
    "AI Deployment Strategy": [
        "Have you decided on an AI deployment model (third-party APIs, in-house AI, or hybrid)?",
        "Is there a structured roadmap for AI implementation, from proof-of-concept (PoC) to full-scale deployment?",
        "Are AI projects integrated into business workflows rather than isolated experiments?"

    ],
    "AI Monitoring & Logging": [
        "Do you continuously monitor AI models for anomalies?",
        "How well-trained is your workforce in identifying and addressing AI security vulnerabilities?",
        "How does your organization handle incidents involving AI security breaches?",
        "How integrated is AI security into your overall cybersecurity strategy?"

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
print("\n🏆 **AI Strategy Readiness Scores:**")
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

print("\n🔹 **Final AI Strategy Readiness Score:**", round(overall_score, 2))
