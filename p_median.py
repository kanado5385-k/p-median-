import pandas as pd
import pulp

# df1 데이터 프레임을 불러오는 코드
df1 = pd.read_excel('/Users/yunbeen/Desktop/중앙공원.xlsx', engine='openpyxl')

def solve_p_median(df1, p):
    # 데이터 프레임에서 'destination' 열을 문자열로 변환
    df1['destination'] = df1['destination'].astype(str)

    # 가능한 'destination' 위치의 목록을 생성
    destinations = list(set(df1['destination'].unique()))

    # 문제 정의
    prob = pulp.LpProblem('p_median', pulp.LpMinimize)

    # 변수 정의
    x = pulp.LpVariable.dicts('x', [(o, d) for o in df1['origin'] for d in destinations], 0, 1, pulp.LpBinary)
    y = pulp.LpVariable.dicts('y', destinations, 0, 1, pulp.LpBinary)

    # 개별 가중치 설정
    weights = {'A': 0.0094, 'B': 0.0018, 'C': 0.0062, 'D': 0.0061, 'E': 0.0124, 'F' : 0.2274, 'G' : 0.2585, 'H' : 0.0223, 'I': 0.0031, 'J' : 0.0317, 'K' : 0.1626, 'L': 0.2585}  # 화물센터/도심지의 가중치 (중요도가 높을수록 가중치 높게)

    # 중심지에 대한 가중치 설정
    center_weights = {'1': 0.0606, '2': 0.0548,'3': 0.0559, '4': 0.0723, '5': 0.0758, '6': 0.0559, '7': 0.0921, '8': 0.0781, '9' : 0.1678, '10' : 0.1655, "11": 0.1212}  # 중심지 가중치 (비용이 낮을수록 가중치 낮게)

    # 목적 함수 설정 (개별 가중치 및 중심지 가중치 포함)
    prob += pulp.lpSum(df1.loc[i, 'distance'] * weights[df1.loc[i, 'origin']] * x[df1.loc[i, 'origin'], df1.loc[i, 'destination']] for i in range(len(df1)))
    prob += pulp.lpSum(center_weights[d] * y[d] for d in destinations)  # 중심지 선택에 대한 추가 비용

    # 제약 조건 추가
    for o in df1['origin'].unique():
        prob += pulp.lpSum(x[o, d] for d in destinations) == 1

    for d in destinations:
        prob += pulp.lpSum(x[o, d] for o in df1['origin'].unique()) <= y[d]

    # 중심지 제약 조건 (정확히 p개의 중심지를 선택)
    prob += pulp.lpSum(y[d] for d in destinations) == p

    # 문제 해결
    prob.solve()

    # 결과 추출
    medians = [d for d in destinations if y[d].value() == 1]
    return medians

# 실행
medians = solve_p_median(df1, 1)
print(medians)

