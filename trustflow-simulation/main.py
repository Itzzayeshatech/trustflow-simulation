import random

# -----------------------------
# TRUSTSCORE CALCULATION
# -----------------------------
def calculate_trust_score(income_stability, repay_history, cash_flow, behavior):
    score = (0.35 * income_stability +
             0.25 * repay_history +
             0.20 * cash_flow +
             0.20 * behavior)
    return int(300 + score * 600)  # scale to 300–900


# -----------------------------
# EMI CALCULATION
# -----------------------------
def calculate_emi(base_emi, income, avg_income):
    adj_factor = max(0.5, min(1.4, income / avg_income))
    emi = base_emi * adj_factor

    # Clamp rules
    emi = min(emi, 0.4 * income)
    emi = max(emi, 0.3 * income)

    return int(emi)


# -----------------------------
# SIMULATION
# -----------------------------
def simulate_users(num_users=1000):
    defaults_static = 0
    defaults_trustflow = 0

    pool = 0

    for _ in range(num_users):
        avg_income = random.randint(20000, 40000)
        income = int(avg_income * random.uniform(0.5, 1.5))

        base_emi = avg_income * 0.2

        # Static EMI default logic
        if base_emi > 0.4 * income:
            defaults_static += 1

        # TrustFlow EMI
        emi = calculate_emi(base_emi, income, avg_income)

        # Pool contribution
        if income > avg_income:
            pool += emi * 0.1
        else:
            if emi > 0.4 * income:
                if pool > emi:
                    pool -= emi
                else:
                    defaults_trustflow += 1

    return defaults_static, defaults_trustflow


# -----------------------------
# RUN
# -----------------------------
if __name__ == "__main__":
    static, trustflow = simulate_users()

    print("Static EMI Defaults:", static)
    print("TrustFlow Defaults:", trustflow)
    print("Reduction (%):", round((static - trustflow) / static * 100, 2))