
xtset pros mm

global X lnewcasenet covid_policy communication reserve_diff exchange_ret  fix_yoy re_yoy usy1diff ///
wti eu bsun stock_pro  cpi_yoy
 

foreach x of global X{        
	xtunitroot ips `x',trend
}

*-----Descriptive statistics.-----
sum2docx c_brdf_r  r_brdf_r i_brdf_r  a_brdf_r  m_brdf_r    n_brdf_r   y1 y10 ///
		using "DS.docx", replace ///
		stats(N mean sd min p25 median p75  max  ) ///
        title("Descriptive statistics.")
		

pvar c_brdf_r  y10 y1  , lags(2) instlags(1/4) fod exog($X) /// 
gmmopts(winitial(identity) wmatrix(robust) twostep vce(cluster pros)) overid
pvarstable
pvargranger
pvarirf,impulse(c_brdf_r) response(y1 y10 )  step(25) tab

pvar r_brdf_r y10 y1, lags(2) instlags(1/4) fod exog($X) /// 
gmmopts(winitial(identity) wmatrix(robust) twostep vce(cluster pros)) overid
pvarstable
pvargranger
pvarirf,impulse(r_brdf_r) response(y1 y10 )  step(25) tab

pvar i_brdf_r  y10 y1  , lags(2) instlags(1/4) fod exog($X) /// 
gmmopts(winitial(identity) wmatrix(robust) twostep vce(cluster pros)) overid
pvarstable

pvar a_brdf_r  y10 y1  , lags(2) instlags(1/4) fod exog($X) /// 
gmmopts(winitial(identity) wmatrix(robust) twostep vce(cluster pros)) overid
pvarstable

pvar m_brdf_r  y10 y1  , lags(2) instlags(1/4) fod exog($X) /// 
gmmopts(winitial(identity) wmatrix(robust) twostep vce(cluster pros)) overid
pvarstable

asdoc pvar m_brdf_r y10 y1, lags(2) instlags(1/4) fod exog($X) /// 
gmmopts(winitial(identity) wmatrix(robust) twostep vce(cluster pros)) , nest rep(se) replace 


*asdoc pvar r_brdf_r y10 y1, lags(2) instlags(1/4) fod exog($X) /// 
*gmmopts(winitial(identity) wmatrix(robust) twostep vce(cluster pros)) , nest rep(se) replace 
