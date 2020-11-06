import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
baseurl = os.path.dirname(os.path.abspath(__file__))


from surprise import Reader, Dataset
from surprise import SVD, NMF
from surprise.model_selection import train_test_split, cross_validate
import pandas as pd

"""
데이터 로딩
surprise data형식에 맞춰 dataframe 변환
"""

df = pd.read_csv("./data/csv/important/db/order_review(remove_userid_nan).csv", sep=",", encoding='utf-8-sig', error_bad_lines=False, engine="python")





# 매장 평점 예측을 위한 데이터 전처리
def prep_shop_model(df):

    """- 필요한 컬럼만 추출"""

    df = df[['userid', 'shop_id', 'taste_rate', 'quantity_rate', 'delivery_rate']]

    """- 합계 평점 컬럼 생성"""

    df['rating'] = (df['taste_rate'] + df['quantity_rate'] + df['delivery_rate'])/3

    """- 세부 평점 컬럼 제거"""

    df = df[['userid', 'shop_id', 'rating']]

    """- 정렬"""

    df_sort = df.sort_values(by=['userid', 'shop_id'], axis=0)

    """- 그룹화"""

    # groupby_df = df_sort.groupby(["userid", 'shop_id'])  # groupby 객체 상태
    df_group = df_sort.groupby(["userid", 'shop_id']).mean()  # groupby 객체 상태
    df = df_group.reset_index()  # reset_index를 해주면 dataframe 객체가 됨

    ''' 예측값과 비교할 때 사용할 실제값 dataframe'''  # keras 모델에서만 사용
    df_backup = df
    # df = groupby_df.head()  # 이유는 모르겠지만 head를 붙였더니 dataframe화 되었음 -> 실수로 인한 잘못된 해결책

    """- 평점이 0인 항목을 제거"""

    df = df.loc[(df.rating != 0)]

    """- 잘 변경 되었는지 확인"""

    df1 = df[df['rating'] == 0]

    """- 유저 리스트 및 유저 수
        - 주의: 일부 유저 연번은 데이터 처리 과정에서 업데이트되어 리뷰 데이터가 없어졌음.
    """

    unique_user_list = df.userid.unique()
    n_users = unique_user_list.shape[0]


    """- 매장 리스트 및 매장 수 조회"""

    unique_shop_list = df.shop_id.unique()
    n_shops = unique_shop_list.shape[0]

    return df

def prep_food_model(df):

    """- 필요한 컬럼만 추출"""

    df = df[['userid', 'food_id', 'taste_rate', 'quantity_rate', 'delivery_rate']]

    """- 합계 평점 컬럼 생성"""

    df['rating'] = (df['taste_rate'] + df['quantity_rate'] + df['delivery_rate'])/3

    """- 세부 평점 컬럼 제거"""

    df = df[['userid', 'food_id', 'rating']]

    """_ food_id 결측된 행 제거 """
    print(df.dtypes)
    df = df.dropna(axis=0)  # 결측값이 들어있는 행 전체 삭제
    
    
    """_ food_id 컬럼 타입 int로 변경 """
    # ' 6746682\n 6746930' > food_id가 여러 개 들어간 경우
    df['food_id'] = df['food_id'].astype(int)


    """- 정렬"""

    df_sort = df.sort_values(by=['userid', 'food_id'], axis=0)

    print(df_sort)

    """- 그룹화"""

    # groupby_df = df_sort.groupby(["userid", 'shop_id'])  # groupby 객체 상태
    df_group = df_sort.groupby(["userid", 'food_id']).mean()  # groupby 객체 상태
    df = df_group.reset_index()  # reset_index를 해주면 dataframe 객체가 됨

    """- 평점이 0인 항목을 제거"""

    df = df.loc[(df.rating != 0)]

    print(df)

    return df



def transform_data(df):
    """### 데이터 변환(Data Transformation)
    - 벡터화 연산을 위해 문자열을 숫자로 변환 필요
    - 유저를 숫자로 변환
    """
    # df.userid = df.userid.astype('category').cat.codes.values  # 향후 확인을 위해 이 방식보다는 map을 사용해야 함
    df['userid'] = df['userid'].map(lambda x: int(x.lstrip('user')))

    return df


def prep_surprise_dataset(df, id_column_name):
    # surprise에서 사용가능하도록  데이터셋 처리
    reader = Reader(rating_scale=(0.5, 5))
    data = Dataset.load_from_df((df[['userid', id_column_name, 'rating']]), reader=reader)
    train, test = train_test_split(data, test_size=0.25, random_state=42)
    # trainset = data.build_full_trainset()

    return data, train, test


#################
# csv 파일 로드
# reader = Reader(line_format='user item rating', sep=',',
#                rating_scale=(0.5, 5))
# data = Dataset.load_from_file('./modeling/model_df.csv',reader=reader)
# trainset = data.build_full_trainset()
# train, test = train_test_split(data, test_size=0.25, random_state=42)
#################



"""
모델 설정 및 학습
"""
def train_model(model, data, train, test):




    # 전체 데이터셋을 학습
    algo = model(n_factors=64, n_epochs=20, random_state=42)
    # cross_validate(algo, data, measures=['rmse', 'mae'], cv=5, verbose=True)
    # model.fit(train)
    algo.fit(train)

    # print(model.test(test))
    return algo



# ###########################
# 매장 추천 관련
# 매장 추천 모델 훅
def hook_shop(df, model):
    df_shop = prep_shop_model(df)
    df_shop = transform_data(df_shop)
    data, train, test = prep_surprise_dataset(df_shop, 'shop_id')
    algo = train_model(model, data, train, test)

    return algo, df_shop

shop_algo, df_shop = hook_shop(df, SVD)

def predict_shop(user, item):
    return shop_algo.predict(user, item)

# ##########################

# ###########################
# 음식 추천 관련
# 음식 추천 모델 훅
def hook_food(df, model):

    df_food = prep_food_model(df)
    df_food = transform_data(df_food)
    data, train, test = prep_surprise_dataset(df_food, 'food_id')
    algo = train_model(model, data, train, test)

    return algo, df_food

food_algo, df_food = hook_food(df, NMF)


def predict_food(user, item):
    return food_algo.predict(user, item)

# ##########################




print('============= 모델 학습 완료 ==============')


"""
예측 및 평가
"""

# # testset = Trainset.build_testset(trainset)
# # prediction_list = model.test(testset)
# pred = model.predict(777, 4960)
# print(pred)
# dump.dump('surprise_svd', predictions=prediction_list, algo=None, verbose=1)

# loaded_model = dump.load('surprise_svd')

# print(loaded_model[0])




# 모듈 내 테스트용
# if __name__ == "__main__":
#     prep_food_model(df)