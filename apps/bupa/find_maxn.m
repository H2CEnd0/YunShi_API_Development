function nmax=find_maxn(r) 
%Ѱ�ҷ�ֵ����nֵ���������� 
%r,���������  
%maxn,Ϊ��ֵ����n  
zer=find(r==0); %�ҵ�һ������������ 
jiaocha=0; %�ҵ�һ����� 
ii=1;  
while (jiaocha<=0)  
    if(r(ii)>0 && r(ii+1)<0 && (ii+1)<length(r)) 
        jiaocha=ii; 
    end
    ii=ii+1;  
    if ii==length(r) %û���ҵ�����Ҫ��ĵ� 
        jiaocha=1; 
    end 
end
if length(zer)>0 %����Ƿ�������  
    if zer(1)<jiaocha %���ڣ����jiaocha�Ƚϴ�С���������ǰ��ĶԻ������ڵĲ��Ҵ�����Ӱ�� 
        jiaocha=zer(1); 
    end
end
r(1:jiaocha)=0; 
%���Ӱ�� 
maxn=max(r); %�����ֵ  
temp=find(r==maxn);%���ص�һ�����ֵ 
nmax=temp(1);
