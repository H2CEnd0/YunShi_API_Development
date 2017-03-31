function nmax=find_maxn(r) 
%寻找峰值最大的n值及基音周期 
%r,自相关序列  
%maxn,为峰值最大的n  
zer=find(r==0); %找第一个零点如果存在 
jiaocha=0; %找第一近零点 
ii=1;  
while (jiaocha<=0)  
    if(r(ii)>0 && r(ii+1)<0 && (ii+1)<length(r)) 
        jiaocha=ii; 
    end
    ii=ii+1;  
    if ii==length(r) %没有找到符合要求的点 
        jiaocha=1; 
    end 
end
if length(zer)>0 %检查是否存在零点  
    if zer(1)<jiaocha %存在，则和jiaocha比较大小，用于祛除前点的对基音周期的查找带来的影响 
        jiaocha=zer(1); 
    end
end
r(1:jiaocha)=0; 
%祛除影响 
maxn=max(r); %找最大值  
temp=find(r==maxn);%返回第一个最大值 
nmax=temp(1);
