/* Dividend-adjusted European Black–Scholes. Rates/volatility are decimals; T is years. */
(function (root) {
  'use strict';
  function cdf(x) {
    const a = Math.abs(x), t = 1 / (1 + 0.2316419 * a);
    const tail = Math.exp(-a * a / 2) / Math.sqrt(2 * Math.PI) * t *
      (0.319381530 + t * (-0.356563782 + t * (1.781477937 + t * (-1.821255978 + t * 1.330274429))));
    return x >= 0 ? 1 - tail : tail;
  }
  function calculate({spot:S, strike:K, time:T, volatility:v, rate:r, dividend:q=0}) {
    if (![S,K,T,v,r,q].every(Number.isFinite) || S <= 0 || K <= 0 || T < 0 || v < 0 || q < 0) {
      throw new RangeError('Use positive prices and non-negative time, volatility and dividend yield.');
    }
    const sd = S * Math.exp(-q*T), kd = K * Math.exp(-r*T);
    if (!Number.isFinite(sd) || !Number.isFinite(kd)) throw new RangeError('Inputs exceed the numerical range of the model.');
    if (T === 0 || v === 0) return {call:Math.max(sd-kd,0),put:Math.max(kd-sd,0),greeks:null};
    const sq = Math.sqrt(T), d1=(Math.log(S/K)+(r-q+v*v/2)*T)/(v*sq), d2=d1-v*sq;
    const density = Math.exp(-d1*d1/2)/Math.sqrt(2*Math.PI);
    // Compute the out-of-the-money option directly, then use parity to reduce cancellation.
    let call,put;
    if(sd >= kd){put=Math.max(0,kd*cdf(-d2)-sd*cdf(-d1));call=put+sd-kd;}
    else{call=Math.max(0,sd*cdf(d1)-kd*cdf(d2));put=call+kd-sd;}
    const diffusion=-sd*density*v/(2*sq);
    return {call,put,greeks:{
      delta:[Math.exp(-q*T)*cdf(d1),-Math.exp(-q*T)*cdf(-d1)],
      gamma:[Math.exp(-q*T)*density/(S*v*sq),Math.exp(-q*T)*density/(S*v*sq)],
      theta:[(diffusion-r*kd*cdf(d2)+q*sd*cdf(d1))/365,(diffusion+r*kd*cdf(-d2)-q*sd*cdf(-d1))/365],
      vega:[sd*density*sq/100,sd*density*sq/100],
      rho:[K*T*Math.exp(-r*T)*cdf(d2)/100,-K*T*Math.exp(-r*T)*cdf(-d2)/100]
    }};
  }
  const api={calculate,cdf};
  if (typeof module !== 'undefined' && module.exports) module.exports=api;
  else root.BlackScholes=api;
})(typeof globalThis !== 'undefined' ? globalThis : this);
