from baby_sleep.contract.models import Child, corrected_age_months


def test_corrected_age_full_term_unchanged():
    # 40 weeks gestation => no correction
    assert corrected_age_months(10, 40) == 10
    assert corrected_age_months(10, None) == 10


def test_corrected_age_preterm_subtracts_prematurity():
    # born at 32 weeks => 8 weeks early ~= 2 months; a 6mo chrono => ~4mo corrected
    assert corrected_age_months(6, 32) == 4


def test_corrected_age_never_negative():
    assert corrected_age_months(1, 28) == 0


def test_child_method_uses_age_months():
    assert Child(age_months=6, gestational_age_at_birth_weeks=32).corrected_age_months() == 4
    assert Child().corrected_age_months() is None
