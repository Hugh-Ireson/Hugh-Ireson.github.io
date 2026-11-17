'use strict';
const form=document.getElementById('calculator-form');
const error=document.getElementById('calc-error');
const fmt=(x,n=4)=>x.toLocaleString('en-NZ',{minimumFractionDigits:n,maximumFractionDigits:n});
function renderChart(inputs){
 const points=Array.from({length:41},(_,i)=>{const spot=inputs.spot*(.5+i/40);return {spot,...BlackScholes.calculate({...inputs,spot})};});
 const max=Math.max(...points.map(p=>Math.max(p.call,p.put)),.01)*1.12;
 const x=(s)=>70+(s/inputs.spot-.5)*660;
 const y=(v)=>280-v/max*245;
 const lines=[];
 for(let i=0;i<=4;i++){const v=max*i/4;lines.push(`<line x1="70" x2="730" y1="${y(v)}" y2="${y(v)}" stroke="#383b35"/><text x="58" y="${y(v)+4}" text-anchor="end">${fmt(v,2)}</text>`);}
 for(let i=0;i<=4;i++){const s=inputs.spot*(.5+i/4);lines.push(`<text x="${x(s)}" y="301" text-anchor="middle">${fmt(s,2)}</text>`);}
 for(const [key,color] of [['call','#f69268'],['put','#dce4ce']]){
  lines.push(`<path d="${points.map((p,i)=>`${i?'L':'M'} ${x(p.spot)} ${y(p[key])}`).join(' ')}" fill="none" stroke="${color}" stroke-width="3"/>`);
 }
 const svg=document.getElementById('sensitivity-chart');
 svg.innerHTML=`<title id="chart-title">Option value against underlying price</title><desc id="chart-desc">Call and put theoretical values for underlying prices from ${fmt(points[0].spot,2)} to ${fmt(points[40].spot,2)}. Remaining inputs held constant. The exact values are in the table below.</desc><g font-family="Arial,sans-serif" font-size="11" fill="#acb0a6">${lines.join('')}<text x="400" y="330" text-anchor="middle">Underlying price</text><text x="70" y="18">Option value per unit</text></g>`;
 document.getElementById('chart-data').innerHTML=points.map(p=>`<tr><td>${fmt(p.spot,2)}</td><td>${fmt(p.call)}</td><td>${fmt(p.put)}</td></tr>`).join('');
}
function clearResults(){
 for(const id of ['call-price','put-price']) document.getElementById(id).textContent='—';
 document.getElementById('greeks').replaceChildren();
 document.getElementById('chart-data').replaceChildren();
 document.getElementById('sensitivity-chart').innerHTML='<title id="chart-title">No sensitivity chart</title><desc id="chart-desc">Enter valid inputs to calculate values.</desc>';
 document.getElementById('result-note').textContent='Enter valid inputs to see results.';
}
function update(){
 error.textContent='';
 if(!form.checkValidity()){clearResults();error.textContent='Complete all inputs within the displayed limits. Prices must be positive; time and volatility may be zero.';return;}
 const values=Object.fromEntries(new FormData(form));
 const inputs={spot:+values.spot,strike:+values.strike,time:+values.days/365,volatility:+values.volatility/100,rate:+values.rate/100,dividend:+values.dividend/100};
 try{
  const result=BlackScholes.calculate(inputs);
  document.getElementById('call-price').textContent=fmt(result.call);
  document.getElementById('put-price').textContent=fmt(result.put);
  document.getElementById('greeks').innerHTML=['delta','gamma','theta','vega','rho'].map(key=>`<tr><th scope="row">${key[0].toUpperCase()+key.slice(1)}</th>${(result.greeks?result.greeks[key]:[null,null]).map(v=>`<td>${v===null?'N/A':fmt(v)}</td>`).join('')}</tr>`).join('');
  document.getElementById('result-note').textContent=inputs.time===0?'At expiry: values equal intrinsic payoff.':inputs.volatility===0?'Zero volatility: discounted deterministic payoff.':'Updated using the inputs shown. Values are per unit, before fees.';
  renderChart(inputs);
 }catch(e){clearResults();error.textContent=e.message;}
}
form.addEventListener('submit',e=>{e.preventDefault();update();});
form.addEventListener('input',update);
form.addEventListener('reset',()=>setTimeout(update,0));
update();
