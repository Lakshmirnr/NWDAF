from app.algorithms.global_metrics import te_signaling_overload, psds

def test_te_sig():
    w = {'N2':[{}]*200, 'N4':[{}]*100, 'SBI':[{}]*50}
    z,_ = te_signaling_overload(w, mu=300, sigma=80)
    assert z >= 0.0

def test_psds():
    w = {'N2':[{'procedure':'X'}], 'SBI':[{'path':'/x'}]}
    g = {'N2_procedures':['A','B'], 'SBI_paths':['/a']}
    val = psds(w, g); assert 0.0 <= val <= 1.0
