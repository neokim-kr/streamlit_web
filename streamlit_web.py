import streamlit as st # 스트림릿 라이브러리 사용
import pandas as pd    # 판다스 라이브러리 사용(데이터 프레임)
import pymysql         # mysql 라이브러리 사용
import plotly.graph_objects as go # 파이썬 그래픽 오브젝트 라이브러리 사용
import datetime        # 날짜 라이브러리 사용
import os              # 터미널 프로그램 라이브러리 사용

#tab_1,tab_2,tab_3 = st.tabs(['Auto Web Program(스케줄)','Auto Web Program(데이터)','Auto Web Program(차트)'])
tab_1,tab_2 = st.tabs(['Auto Web Program(스케줄)','Auto Web Program(시나리오 데이터)'])

def get_schedule(start_day,end_day,start_time,end_time):
    #변수 선언
    conn, cur = None, None

    # connect database
    conn = pymysql.connect(host='127.0.0.1', user='root', password='12345678',db='appium',charset='utf8')

    # create cursor
    cur = conn.cursor()

    if start_time == '':
        sql_1 = " with Table_2 as ("
        sql_2 =	"   with Table_1 as ("
        sql_3 =	"					select time_name, start_time,end_time,sleep_time,script_cd,if(error_cd != '0000', '오류','성공') as error_result, run_time" 
        sql_4 =	"					from appium.appium_tb" 
        sql_5 =	"					where (reg_time >= " + "'" + str(start_day) + "'" + " or reg_time = " + "'" + str(end_day) + "'" + ")" 
        sql_6 =	"					group by time_name,script_cd,sleep_time,start_time,end_time,  error_result , run_time"
        sql_7 =	"				    )"
        sql_8 =	"			select time_name,script_cd,error_result,start_time,end_time,run_time from Table_1"
        sql_9 =	"			group by time_name,script_cd,error_result,start_time,end_time,run_time" 
        sql_10 = "	)"
        sql_11 = "	select time_name,sum(script_cd)as script_cd,sum(success_cnt)as success_cnt,sum(error_cnt)as error_cnt,start_time,end_time,run_time from ("
        sql_12 = "		select time_name,count(script_cd)as script_cd,count(case when error_result = '성공' then 1 end) as success_cnt,count(case when error_result = '오류' then 1 end) as error_cnt"  
        sql_13 = "		      ,start_time,end_time,run_time"
        sql_14 = "		from Table_2"
        sql_15 = "		group by time_name,script_cd,start_time,end_time,run_time"
        sql_16 = "	) Table_3"
        sql_17 = "	group by time_name,script_cd,start_time,end_time,run_time"
        total_sql = sql_1 + sql_2 + sql_3 + sql_4 + sql_5 + sql_6 + sql_7 + sql_8 + sql_9 + sql_10 + sql_11 + sql_12 + sql_13 + sql_14 + sql_15 + sql_16 + sql_17      
    else:
        sql_0 = " select * from ("
        sql_1 = " with Table_2 as ("
        sql_2 =	"   with Table_1 as ("
        sql_3 =	"					select time_name, start_time,end_time,sleep_time,script_cd,if(error_cd != '0000', '오류','성공') as error_result, run_time" 
        sql_4 =	"					from appium.appium_tb" 
        sql_5 =	"					where (reg_time >= " + "'" + str(start_day) + "'" + " or reg_time = " + "'" + str(end_day) + "'" + ")" 
        sql_6 =	"					group by time_name,script_cd,sleep_time,start_time,end_time,  error_result , run_time"
        sql_7 =	"				    )"
        sql_8 =	"			select time_name,script_cd,error_result,start_time,end_time,run_time from Table_1"
        sql_9 =	"			group by time_name,script_cd,error_result,start_time,end_time,run_time" 
        sql_10 = "	)"
        sql_11 = "	select time_name,sum(script_cd)as script_cd,sum(success_cnt)as success_cnt,sum(error_cnt)as error_cnt,start_time,end_time,run_time from ("
        sql_12 = "		select time_name,count(script_cd)as script_cd,count(case when error_result = '성공' then 1 end) as success_cnt,count(case when error_result = '오류' then 1 end) as error_cnt"  
        sql_13 = "		      ,start_time,end_time,run_time"
        sql_14 = "		from Table_2"
        sql_15 = "		group by time_name,script_cd,start_time,end_time,run_time"
        sql_16 = "	) Table_3"
        sql_17 = "	group by time_name,script_cd,start_time,end_time,run_time"
        sql_18 = " ) Table_4"

        sql_19 = " where start_time  = " + "'" + str(start_time) + "'" + " and end_time  = " + "'" + str(end_time) + "'" 
        # sql_20 = " and  script_cd   = " + "'" + str(script_cd) + "'" 
        # sql_21 = " and start_time  = " + "'" + str(start_time) + "'" + " and end_time  = " + "'" + str(end_time) + "'" 
        # sql_22 = " and  script_cd   = " + "'" + str(script_cd) + "'"         
        #sql_21 = " and  error_cd   = "  + "'" + str(error_cd) + "'" 
        

        total_sql = sql_0 + sql_1 + sql_2 + sql_3 + sql_4 + sql_5 + sql_6 + sql_7 + sql_8 + sql_9 + sql_10 + sql_11 + sql_12 + sql_13 + sql_14 + sql_15 + sql_16 + sql_17 + sql_18 + sql_19  

    print('[get_schedule_total_sql]' + str(total_sql))
    
    #os.system("pause")
    cur.execute(total_sql)

    rows = cur.fetchall()

    #sconn.close() # DB 연결 종료
    

    data = pd.read_sql(total_sql,conn)
    
    data.rename(columns={
                       'script_cd':'시나리오(건수)',
                       'time_name':'스케줄명',
                       'sleep_time':'반복주기',
                       'success_cnt':'성공(건수)',
                       'error_cnt':'실패(건수)',
                       'start_time':'시작시간(시간)',
                       'end_time':'종료시간(시간)',
                       'run_time':'소요시간(초)',
                       'one_day':'등록일자',
                       'error_result':'성공여부'
                      }
              ,inplace=True)

    df = pd.DataFrame(data)

    # num_rows = len(df)
    # for i in range(num_rows):
    #     st.write(df.iloc[i], height=300)

    st.dataframe(df)

    conn.close()

def get_grid(start_day,end_day,start_time,end_time):
    #변수 선언
    conn, cur = None, None

    # connect database
    conn = pymysql.connect(host='127.0.0.1', user='root', password='12345678',db='appium',charset='utf8')

    # create cursor
    cur = conn.cursor()

    if start_time == '':
        sql_1 = "select time_name,script_cd,step_basic_cd,step_detail_cd,if(error_cd != '0000', '오류','성공') as error_result,send_id,recv_id,email_title,email_contents  from appium.appium_tb "
        sql_2 = " where (reg_time >= " + "'" + str(start_day) + "'" + " or reg_time = " + "'" + str(end_day) + "'" + ")" 

        total_sql = sql_1 + sql_2
    else:
        sql_1 = "select time_name,script_cd,step_basic_cd,step_detail_cd,if(error_cd != '0000', '오류','성공') as error_result,send_id,recv_id,email_title,email_contents  from appium.appium_tb "
        sql_2 = " where (reg_time >= " + "'" + str(start_day) + "'" + " or reg_time = " + "'" + str(end_day) + "'" + ")" 
        sql_3 = " and start_time  = " + "'" + str(start_time) + "'" + " and end_time  = " + "'" + str(end_time) + "'" 
        #sql_4 = " and  script_cd   = " + "'" + str(script_cd) + "'" 
        #sql_5 = " and  error_cd   = "  + "'" + str(error_cd) + "'" 

        total_sql = sql_1 + sql_2 + sql_3 

    print('[get_grid_total_sql]' + str(total_sql))

    cur.execute(total_sql)

    rows = cur.fetchall()

    #sconn.close() # DB 연결 종료

    #print(rows)
    df = pd.read_sql(total_sql,conn)
    
    
    #df.columns = df.columns.str.center(len(df.columns[1]))
    #df.columns = pd.MultiIndex.from_tuples([(col, '<center>') for col in df.columns])
    #df.columns = ['send_id','recv_id']
    
    
    df.rename(columns={'send_id':'보내는사람(email)',
                       'recv_id':'받는사람(email)',
                       'email_title':'메일제목',
                       'email_contents':'메일내용',
                       'step_basic_cd':'기본진행코드',
                       'step_detail_cd':'상세진행코드',
                       'error_cd':'오류코드',
                       'error_msg':'오류메시지',
                       'reg_time':'등록시간',
                       'script_cd':'시나리오코드',
                       'time_name':'스케줄명',
                       'sleep_time':'반복주기',
                       'success_cnt':'성공',
                       'error_cnt':'실패',                       
                       'start_time':'시작시간',
                       'end_time':'종료시간',
                       'run_time':'소요시간',
                       'one_day':'등록일자',
                       'error_result':'성공여부'
                      }
             ,inplace=True)
    
    #df.to_string(justify='center')
    #df.style.set_properties({'text-align':'center'}).set_table_styles([dict(selector='th',props=[('text-align','center')])])
    #df.style.set_properties(align="center")

    #df = pd.DataFrame(df)
    #sty_df = df.style.set_properties(**{'text-align':'center'})
    
    st.dataframe(df)
    
    conn.close()

def get_chart():

    # 데이터
    query_1 = [['2023-07-11','2023-07-12','2023-07-13','2023-07-14','2023-07-15']
            ]
    query_2 = [[20,30,40,25,15] # success count
            ]
    query_3 = [[4,6,8,5,3]      # error count
            ]

    # query_3 = [['2023-07-02',20]
    #         ]
    # query_4 = [['2023-07-02',6]
    #         ]
    
    # query_5 = [['2023-07-03',15]
    #         ]
    # query_6 = [['2023-07-03',4]
    #         ]

    df_d = pd.DataFrame(query_1, columns=['Date1','Date2','Date3','Date4','Date5'])
    df_s = pd.DataFrame(query_2, columns=['success1','success2','success3','success4','success5'])
    df_e = pd.DataFrame(query_3, columns=['error1','error2','error3','error4','error5'])

    # df_3 = pd.DataFrame(query_3, columns=['Date','success'])
    # df_4 = pd.DataFrame(query_4, columns=['Date','error'])

    # df_5 = pd.DataFrame(query_5, columns=['Date','success'])
    # df_6 = pd.DataFrame(query_6, columns=['Date','error'])

    # 차트
    data_1 = go.Bar(x=df_d['Date1'],y=df_s['success1'], marker={'color':'#0067a3'}, name='성공(2023-07-11)')
    data_2 = go.Bar(x=df_d['Date1'],y=df_e['error1']  , marker={'color':'#ff0000'}, name='실패(2023-07-11)')

    data_3 = go.Bar(x=df_d['Date2'],y=df_s['success2'], marker={'color':'#0067a3'}, name='성공(2023-07-12)')
    data_4 = go.Bar(x=df_d['Date2'],y=df_e['error2']  , marker={'color':'#ff0000'}, name='실패(2023-07-12)')

    data_5 = go.Bar(x=df_d['Date3'],y=df_s['success3'], marker={'color':'#0067a3'}, name='성공(2023-07-13)')
    data_6 = go.Bar(x=df_d['Date3'],y=df_e['error3']  , marker={'color':'#ff0000'}, name='실패(2023-07-13)')

    layout = go.Layout(title='Web Atuo Program')
    
    #fig = go.Figure(data=[data_1,data_2,data_3,data_4,data_5,data_6], layout=layout)
    fig = go.Figure(data=[data_1,data_2,data_3,data_4,data_5,data_6])

    #fig.show()
    st.write(fig)


# 프로그램 시작부분
if __name__ == '__main__':

    # 타이틀
    st.sidebar.title('Web Auto Program')

    # 날짜
    date_start_day = st.sidebar.date_input("시작 날짜를 선택하세요", datetime.datetime.now())
    #st.sidebar.text('~')
    date_end_day = st.sidebar.date_input("종료 날짜를 선택하세요", datetime.datetime.now())

    chkbox_option = st.sidebar.checkbox("데이터 조회 옵션을 선택하세요")

    # 옵션 체크박스
    if chkbox_option == True:
        print('선택')
        selbox_start_time = st.sidebar.selectbox('시작 시간을 선택해주세요',['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23'])
        selbox_end_time = st.sidebar.selectbox('종료 시간을 선택해주세요',['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23'])

        #selbox_script_cd = st.sidebar.selectbox('시나리오 스크립트 코드를 선택해주세요',['1','2','3','4','5','6','7','8','9','10'])

        #selbox_success_yn = st.sidebar.selectbox('성공여부를 선택해주세요',['성공','실패'])        
    else:
        print('미선택')
        selbox_start_time = ''
        selbox_end_time   = ''
        #selbox_script_cd  = ''
        #selbox_success_yn = ''
    
    button = st.sidebar.button("조회")
    st.sidebar.write()

    # 그리드 체크했을때 상세화면 출력
    # streamlit-aggrid를 사용해서 테이블 상호작용되도록 코딩해야함
    
    # 버튼을 눌렀을때
    if button:

        print('[date_start_day]' + str(date_start_day))
        print('[date_end_day]'   + str(date_end_day))
        print('[selbox_start_time]' + str(selbox_start_time))
        print('[selbox_end_time]' + str(selbox_end_time))
        #print('[selbox_script_cd]' + str(selbox_script_cd))
        #print('[selbox_success_yn]' + str(selbox_success_yn))        
        # if str(selbox_success_yn) == "성공":
        #     print('0000')
        #     error_cd = '0000'
        # else:
        #     print('9999')
        #     error_cd = '9999'

        with tab_1:
            #st.write('Auto Web Program(스케줄)')
            get_schedule(date_start_day,date_end_day,selbox_start_time,selbox_end_time)    
        with tab_2:
            #st.write('Auto Web Program(데이터)')
            get_grid(date_start_day,date_end_day,selbox_start_time,selbox_end_time)
        
        # with tab_3:
        #     #st.write('Auto Web Program(차트)')
        #     get_chart()
    
    #st.sidebar.write()
