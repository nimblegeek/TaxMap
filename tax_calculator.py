def calculate_tax_distribution(monthly_salary, tax_rates):
    annual_salary = monthly_salary * 12
    
    # Unpack tax rates
    _, state, federal_rate, state_rate, local_rate, social_security_rate, medicare_rate = tax_rates

    # Calculate taxes
    federal_tax = annual_salary * (federal_rate / 100)
    state_tax = annual_salary * (state_rate / 100)
    local_tax = annual_salary * (local_rate / 100)
    social_security_tax = min(annual_salary * (social_security_rate / 100), 8853.60)  # 2021 cap
    medicare_tax = annual_salary * (medicare_rate / 100)

    total_tax = federal_tax + state_tax + local_tax + social_security_tax + medicare_tax
    net_income = annual_salary - total_tax

    return {
        'gross_income': round(annual_salary, 2),
        'federal_tax': round(federal_tax, 2),
        'state_tax': round(state_tax, 2),
        'local_tax': round(local_tax, 2),
        'social_security_tax': round(social_security_tax, 2),
        'medicare_tax': round(medicare_tax, 2),
        'total_tax': round(total_tax, 2),
        'net_income': round(net_income, 2)
    }
