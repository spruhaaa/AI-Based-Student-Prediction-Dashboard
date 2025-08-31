import pandas as pd
import numpy as np

np.random.seed(42)
n = 1000

df = pd.DataFrame({
    'student_id': range(1, n+1),
    'attendance_percent': np.random.randint(50, 100, n),
    'internal_marks': np.random.randint(20, 40, n),
    'past_sem_marks': np.random.randint(40, 100, n),
    'final_result': np.random.choice(['Pass', 'Fail'], n, p=[0.85, 0.15])
})

df.to_csv('student_data.csv', index=False)
