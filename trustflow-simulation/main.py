import streamlit as st
import random
import matplotlib.pyplot as plt

# -----------------------------
# EMI CALCULATION
# -----------------------------
def calculate_emi(base_emi, income, avg_income):
    adj_factor = max(0.5, min(1.4, income / avg_income))
    emi = base_emi * adj_factor

    # Clamp rules
    emi = min(emi, 0.4 * income)
    emi = max(emi, 0.3 * income)

    return emi


# -----------------------------
# SIMULATION (TUNED FOR REALISM)
# -----------------------------
def simulate_users(num_users=1000):
    defaults_static = 0
    defaults_trustflow = 0

    pool = 0
    POOL_LIMIT = 100000  # reduced pool → realistic

    for _ in range(num_users):
        avg_income = random.randint(20000, 40000)

        # more realistic income volatility
        income = int(avg_income * random.uniform(0.4, 1.4))

        base_emi = avg_income * 0.3  # slightly aggressive EMI

        # -----------------
        # STATIC EMI DEFAULT
        # -----------------
        if base_emi > 0.3 * income:
            defaults_static += 1

        # -----------------
        # TRUSTFLOW EMI
        # -----------------
        emi = calculate_emi(base_emi, income, avg_income)

        # -----------------
        # POOL LOGIC
        # -----------------
        if income > avg_income:
           pool += emi * 0.03
           pool = min(pool, POOL_LIMIT)

        else:
            if emi > 0.3 * income:

                # partial support only
                if pool > emi * 0.2:
                   pool -= emi * 0.2

                    # higher probability of default (important)
                   if random.random() < 0.85:
                        defaults_trustflow += 1
                else:
                    defaults_trustflow += 1

    return defaults_static, defaults_trustflow


# -----------------------------
# GRAPH FUNCTION
# -----------------------------
def plot_results(static, trustflow):
    labels = ['Static EMI', 'TrustFlow']
    values = [static, trustflow]

    plt.figure()
    plt.bar(labels, values)
    plt.title("Default Comparison")
    plt.xlabel("Model")
    plt.ylabel("Number of Defaults")

    st.pyplot(plt)


# -----------------------------
# STREAMLIT UI
# -----------------------------
st.title("🚀 TrustFlow AI Simulation")
st.write("Adaptive EMI vs Traditional EMI (Default Comparison)")

users = st.slider("Number of Users", 100, 5000, 1000)

if st.button("Run Simulation"):
    static, trustflow = simulate_users(users)

    st.write("### 📊 Results")
    st.write("Static EMI Defaults:", static)
    st.write("TrustFlow Defaults:", trustflow)

    if static == 0:
        st.write("Reduction (%): No defaults")
    else:
        reduction = (static - trustflow) / static * 100
        st.write("Reduction (%):", round(reduction, 2))

    plot_results(static, trustflow)