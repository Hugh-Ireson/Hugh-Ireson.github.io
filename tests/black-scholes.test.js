const {test}=require('node:test');
const assert=require('node:assert/strict');
const {calculate}=require('../assets/black-scholes.js');
const base={spot:100,strike:100,time:1,volatility:.2,rate:.05,dividend:0};
const near=(a,b,t=1e-4)=>assert.ok(Math.abs(a-b)<t,`${a} != ${b}`);
test('standard reference prices and Greeks',()=>{const p=calculate(base);near(p.call,10.450583572);near(p.put,5.573526022);near(p.greeks.delta[0],.636830651);near(p.greeks.gamma[0],.018762017);near(p.greeks.vega[0],.375240347);near(p.greeks.theta[0],-.017572678);near(p.greeks.rho[0],.532324815);});
test('dividends and negative rates preserve put-call parity and price bounds',()=>{
 for(const spot of [1,80,100,150,10000])for(const volatility of [.01,.2,2])for(const rate of [-.05,.05]){
 const p={...base,spot,volatility,rate,dividend:.03};const v=calculate(p);const sd=spot*Math.exp(-p.dividend),kd=100*Math.exp(-rate);
 near(v.call-v.put,sd-kd,1e-7);assert.ok(v.call>=0&&v.call<=sd+1e-7);assert.ok(v.put>=0&&v.put<=kd+1e-7);
 }
});
test('expiry and zero volatility use the correct limiting payoff',()=>{assert.deepEqual(calculate({...base,time:0,spot:120}),{call:20,put:0,greeks:null});const v=calculate({...base,volatility:0});near(v.call,100-100*Math.exp(-.05));near(v.put,0);assert.equal(v.greeks,null);});
test('Greeks agree with finite differences',()=>{const p={...base,dividend:.02};const v=calculate(p);const h=.001;for(const [i,key] of ['call','put'].entries()){
 near((calculate({...p,spot:p.spot+h})[key]-calculate({...p,spot:p.spot-h})[key])/(2*h),v.greeks.delta[i],2e-5);
 near((calculate({...p,volatility:p.volatility+h})[key]-calculate({...p,volatility:p.volatility-h})[key])/(2*h*100),v.greeks.vega[i],2e-5);
 near((calculate({...p,rate:p.rate+h})[key]-calculate({...p,rate:p.rate-h})[key])/(2*h*100),v.greeks.rho[i],2e-5);
 near(-(calculate({...p,time:p.time+h})[key]-calculate({...p,time:p.time-h})[key])/(2*h*365),v.greeks.theta[i],2e-5);
 }});
test('invalid model inputs are rejected',()=>{for(const patch of [{spot:0},{strike:-1},{time:-1},{volatility:-1},{spot:NaN},{rate:Infinity}])assert.throws(()=>calculate({...base,...patch}),RangeError);});
