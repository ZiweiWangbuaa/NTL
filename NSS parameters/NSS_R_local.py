import pandas as pd
import numpy as np
from scipy.optimize import minimize
import numpy as np
import pandas as pd 


def cal_yield_to_maturity(current_price:float, face_value:float, interest:float,t_list:list,frequency:float)->float:
    '''
     Function: Calculate Yield to Maturity
     parameter: current_price:float, face_value:float, interest(face):float, t_list(time_list):list, frequency:float
     return:
        yields(float): Yield to maturity
     '''
    def objective_function(r:float):
        '''
        Function: The function is to make the current bond price equal to the present value of the bond
        parameter: r:float(iteration)
        return:
            error(float): (\hat(e)-e)^2
        '''
        pv = [interest/(1+r)**t for t in t_list]
        pv[-1] = pv[-1] + face_value/(1+r)**t_list[-1]
        price_hat = np.sum(pv)
        error = (price_hat - current_price)**2
        return error

    # Use scipy.optimize.minimize to find the minimum of the objective function
    yields = minimize(objective_function, x0=0.05, method='Nelder-Mead').x[0] 
    return yields/frequency

def cal_pv( face_value:float, interest:float,t_list:list,r:float)->list:
    '''
    Function: Calculate the present value
    parameter: face_value:float, interest(face):float, t_list(time_list):list, r(discount rate):float
    return:
        present value(float):\sum_1^T{i/(1+r)^t}+fv/(1+r)^T
    '''    
    try:
        t_list.remove(0.0)
    except:
        pass
    pv = [interest/(1+r)**t for t in t_list]
    pv[-1] = pv[-1] + face_value/(1+r)**t_list[-1]
    return pv

def NSS(m,vi):
    '''
    Function: NSS model
    return: r
    '''       
    b0, b1, b2 ,b3 , tau1, tau2 = vi
    r = b0 + b1*((1-np.exp(-m/tau1))/(m/tau1)) +b2*((1-np.exp(-m/tau1))/(m/tau1)- np.exp(-m/tau1)) + b3*((1-np.exp(-m/tau2))/(m/tau2) - np.exp(-m/tau2))
    return r 

def NSS_r_error(m:float,vi:list,yields:float)->float:
    '''
    Function: the error^2 between yield and r(NSS model) of one bond
    return: error^2
    ''' 
    r = NSS(m,vi)
    e = ((yields-r)*100)**2
    return e
def nss_error_sum(vi, *args):
    '''
    Function: the sum of the error^2 between yield and r(NSS model) of all bond, scaled by n^2
    return: sum(error^2)/n^2
    ''' 
    df0, = args 
    e = df0.apply(lambda x:NSS_r_error(x['TTM'],vi,x['YTM']),axis=1)
    return np.sum(e)/len(e)/len(e)

def nss_fit(vi,df0):
    def nss_r_constraint(vi):
        '''
        constraint: 0<r(m)<0.05, exp(-r(m1)*m1)>exp(-r(m2)*m2), if m2>m1
        ''' 
        r = [NSS(0.001,vi)-0.0001 ]
        r = r+[NSS(m/10,vi)-0.0001 for m in range(1,100) ]
        r = r+[0.05-NSS(0.001,vi)]
        r = r+[0.05-NSS(m/10,vi) for m in range(1,100) ]
        for m in range(100):
            r.append(np.exp(-r[m]*(m/10))-np.exp(-r[m+1]*(m+1)/10))
        return r
    bounds = ((0.01,0.08), (-30, 30), (-30, 30), (-30, 30), (0.0001, 30),(0.0001,30))
    result = minimize(nss_error_sum, vi,constraints={'type': 'ineq', 'fun': nss_r_constraint},
                    bounds=bounds,args=(df0),tol=0.000000001,options={'maxiter':1000000000},\
                    method = 'SLSQP')    
    return  result.x,result.fun

def remove_outliers(df):
    '''
    Function: calculate the boundary of outliers.
        1. Sub-boxes, 100 pieces.
        2. Find the weekly standard deviation for each bin
        3. Boundary: mean plus or minus two standard deviations
    return: dataframe, boundary for each bin
    ''' 
    # Identify the year and week
    df['YW']=pd.to_datetime(df['Date']).dt.year.astype(str)+pd.to_datetime(df['Date']).dt.week.astype(str)
    a1 = df[['YW','YTM','TTM']]
    bins = [b/2 for b in range(100)]
    labels = bins 
    a1.loc[:,'cut'] = pd.cut(x = a1['TTM'], bins = bins, labels = labels[1:], include_lowest = True)
    # mean for each bin in each week 
    a2= a1.groupby(['cut','YW'],as_index=False).mean().dropna()
    del a2['TTM']
    a2.columns=['cut','YW','AYTM']
    # std for each bin in each week 
    a3= a1.groupby(['cut','YW'],as_index=False).std().dropna()
    del a3['TTM']
    a3.columns=['cut','YW','StdYTM']
    # merge the boundary
    a4 = a3[['cut','YW']]
    a4['UPYTM']=a2['AYTM']+2*a3['StdYTM']
    a4['LOWYTM']=a2['AYTM']-2*a3['StdYTM']
    return a4

for pr in ['Anhui','Beijing','Fujian','Gansu','Guangdong','Guangxi','Guizhou','Hainan','Hebei','Henan','Heilongjiang','Hubei','Hunan','Jilin','Jiangsu','Jiangxi','Liaoning','Neimenggu','Ningxia','Qinghai','Shandong','Shaanxi','Shanxi','Shanghai','Sichuan','Tianjin','Xizang','Xinjiang','Yunnan','Zhejiang','Chongqing']:
    df = pd.read_csv("{}.csv".format(pr))
    df['Date'] = pd.to_datetime(df['Date'])
    # 0<YTM<0.05
    df = df[(df["YTM"]>0) & (df["YTM"]<0.05) & (df['Date']>pd.to_datetime("2013-12-31"))]
    # to remove outliers, return the boundary
    a4 = remove_outliers(df)
    date_list = pd.date_range(start="20150101", end="20221231",freq='D').strftime("%Y-%m-%d").tolist() 
    for i in range(len(date_list)):
        # select all samples for one day
        df2 = df# [(df['TTM']>=1) ]
        df2 = df2[pd.to_datetime(df2['Date'])==pd.to_datetime(date_list[i])]
        try:
            # sample size > 10
            if df2.shape[0]>10:
                bins = [b/2 for b in range(100)]
                labels = bins 
                df2.loc[:,'cut'] = pd.cut(x = df2['TTM'], bins = bins, labels = labels[1:], include_lowest = True)
                df2.loc[:,'DiscountYear'] = df2['DiscountYear'].apply(lambda x: [float(xx) for xx in eval(x)])
                # merge the boundaries
                df2 = pd.merge(df2,a4,on=['YW','cut'])
                # remove outliers
                df2 = df2[df2['YTM']<df2['UPYTM']]
                df2 = df2[df2['YTM']>df2['LOWYTM']]
                # set initial values
                b0 = np.max(df2['YTM'])
                b1 = np.max(df2['YTM']) - np.min(df2['YTM'])
                b2 = 2*np.mean(df2['YTM'])-np.max(df2['YTM']) - np.min(df2['YTM'])
                b3 = b2
                tau1 = 1
                tau2 = 1
                vi = [b0,b1,b2,b3,tau1,tau2]
                if df2.shape[0]>10:
                    # calculate NSS parameters
                    param,f = nss_fit(vi,df2)
                    a = pd.DataFrame(param).T
                    a['fun'] = f
                    a['date'] = date_list[i]
                    a.to_csv("NSS_R_nls_{}(std2).csv".format(pr),encoding="utf-8-sig",mode="a",index=None,header=None)
        except BaseException as err:
            print(err)
