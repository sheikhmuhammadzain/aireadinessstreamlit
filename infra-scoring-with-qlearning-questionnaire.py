import numpy as np

# ✅ Hardcoded Questionnaire (Categorized)
questionnaire = {
    "Compute Resources": [
        "Do you have the necessary GPUs/TPUs for AI workloads?",
        "Are your compute resources sufficient for AI training tasks?",
        "Do you have redundancy systems for AI computing needs?",
        "How aligned are your hardware upgrades with AI goals?",
        "Do you have a separate budget for scaling AI infrastructure?"

    ],
    "Storage & Data Access": [
        "Is your data storage optimized for AI scalability?",
        "Do you have dedicated data lakes for AI use cases?",
        "Is your storage optimized for unstructured data used in AI?",
        "How robust are your backup systems for AI data and models?",
        "Do you have a disaster recovery plan specific to AI workloads?"
    ],
    "AI Deployment Efficiency": [
        "Have you implemented containerization & orchestration for AI models?",
        "Do you use containerization tools for AI model deployment?",
        "Are your AI systems interoperable across teams and departments?",
        "Is your infrastructure compliant with global AI standards?",
        "Is your IT infrastructure cloud-compatible for scaling AI?"
    ],
    "HPC & Performance Optimization": [
        "Are distributed computing techniques used for AI acceleration?",
        "Is there a plan to adopt edge computing for AI workloads?",
        "Are distributed computing techniques used for AI acceleration?",
        "How efficiently does your infrastructure support real-time AI operations?",
        "Do you use benchmarking tools to assess infrastructure for AI readiness?",
        "Do you have latency monitoring systems for AI services?"
    ],
    "MLOps Readiness": [
        "Is there an automated AI model monitoring & retraining process?",
        "Is there an AI-specific network architecture in place?",
        "Are your AI systems integrated with IoT platforms?",
        "Is your IT team trained in managing AI-specific workloads?",
        "Do you evaluate the environmental impact of AI infrastructure?"
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
print("\n🏆 **AI Infrastructure Readiness Scores:**")
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

print("\n🔹 **Final AI Infrastructure Readiness Score:**", round(overall_score, 2))
