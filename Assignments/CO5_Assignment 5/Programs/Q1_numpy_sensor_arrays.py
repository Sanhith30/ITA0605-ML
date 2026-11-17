"""Q1: Array properties, vectorisation, broadcasting, RNG and view/copy verification."""
import numpy as np
from common import OUT, DATA, save_json
np.set_printoptions(precision=4, suppress=True, linewidth=105)

def main():
    temp = np.array([[70,72,75,71,90], [65,66,64,67,66],
                     [80,82,85,88,91], [60,61,59,62,60]], dtype=np.int64)
    np.savetxt(DATA/'Q1_original_machine_temperatures.csv', temp, delimiter=',', fmt='%d')
    alt = np.array([70,72,75,71,90,65,66,64,67,66,80,82,85,88,91,60,61,59,62,60]).reshape(4,5)
    f32 = temp.astype('float32')
    fahrenheit = temp*9/5+32
    changes = temp[:,1:] - temp[:,:-1]
    machine_means = temp.mean(axis=1, keepdims=True)
    centered = temp - machine_means
    seed = 20260501
    errors = np.random.default_rng(seed).normal(0, .5, (4,5))
    same_errors = np.random.default_rng(seed).normal(0, .5, (4,5))
    measured = temp + errors
    sqrt_abs = np.sqrt((temp-machine_means)**2)  # absolute deviation via sqrt of squared values
    exp_confidence = np.exp(-sqrt_abs/10)         # decays as temperature deviates from mean
    log_above_50 = np.log(temp - 50)              # defined: all readings > 50
    rounded_f = np.round(fahrenheit, 1)
    clipped_temp = np.clip(temp, 60, 85)
    heat_alert = np.where(temp >= 85, 'HOT', 'OK')
    view_base = temp.copy()
    basic_view = view_base[:2, :2]
    basic_view[0,0] = 999
    fancy_copy = temp[[0,1],:2]
    fancy_copy[0,0] = -99
    assert view_base[0,0] == 999 and temp[0,0] == 70
    assert np.array_equal(temp, alt) and np.array_equal(errors, same_errors)
    res = dict(shape=list(temp.shape), ndim=temp.ndim, size=temp.size, dtype=str(temp.dtype),
               original_nbytes=temp.nbytes, float32_dtype=str(f32.dtype), float32_nbytes=f32.nbytes,
               equal_second_construction=bool(np.array_equal(temp,alt)),
               predicted_shapes={'fahrenheit':[4,5],'day_change':[4,4],'machine_means':[4,1],
                  'centered':[4,5], 'errors':[4,5], 'measured':[4,5], 'five_functions':[4,5]},
               fahrenheit=fahrenheit, day_changes=changes, machine_means=machine_means.ravel(),
               centered=centered, errors=errors, measured=measured,
               seeded_repeat_identical=bool(np.array_equal(errors,same_errors)),
               functions={'sqrt_abs_deviation':sqrt_abs,'exp_confidence':exp_confidence,
               'log_temp_minus_50':log_above_50,'round_fahrenheit':rounded_f,
               'clip_60_to_85':clipped_temp,'where_hot':heat_alert},
               view_changes_parent=int(view_base[0,0]), fancy_copy_leaves_original=int(temp[0,0]))
    save_json(1,res)
    print('Q1 ORIGINAL ARRAY\n',temp)
    print('Shape/dimensions/size/type/bytes:',temp.shape,temp.ndim,temp.size,temp.dtype,temp.nbytes)
    print('Float32 bytes:',f32.nbytes,'alternative construction equal:',res['equal_second_construction'])
    print('FAHRENHEIT\n',fahrenheit)
    print('DAY-TO-DAY CHANGES\n',changes)
    print('BROADCAST MACHINE MEANS (4,1)\n',machine_means)
    print('CENTERED (4,5)\n',centered)
    print('SEEDED ERRORS\n',errors)
    print('SEEDED REPEAT EQUAL:',res['seeded_repeat_identical'])
    print('MEASURED WITH ERRORS\n',measured)
    print('np.sqrt(abs deviation)\n',sqrt_abs)
    print('np.exp(deviation confidence)\n',exp_confidence)
    print('np.log(temperature-50)\n',log_above_50)
    print('np.round(Fahrenheit,1)\n',rounded_f)
    print('np.clip(temperature,60,85)\n',clipped_temp)
    print('np.where(hot >=85)\n',heat_alert)
    print('BASIC SLICE VIEW CHANGES PARENT TO:',view_base[0,0])
    print('FANCY INDEX COPY LEAVES ORIGINAL AT:',temp[0,0])

if __name__=='__main__': main()
