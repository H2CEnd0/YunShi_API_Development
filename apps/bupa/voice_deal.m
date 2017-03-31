function [ output ] = voice_deal ( Path_data , File_number )
%% �������
data_deal.Fs=10000;                     %�����ز���Ƶ�ʣ������źŷ�ΧΪ300~3400HZ��
data_deal.FFT.N=0;                      %����Ҷ��Nֵ����0�Ļ���ʹ��Ĭ���źų��ȣ�
data_deal.Filter.a=-0.9375;             %��ͨ�˲�����Ԥ����ϵ��
data_deal.start=1;                      %��ʼ��ȡ����1s��
data_deal.Windowing.window='Hamming';   %�Ӵ�������:'Hamming':������
data_deal.Windowing.step=10;            %����֡�ƣ���λ/ms��
data_deal.Windowing.framelength=25;     %����ʱ�䳤�ȣ���λ/ms��
data_deal.Silent.E=[0.02,0.05];         %����������ޣ������޺͸����ޣ�
%% ���ݶ�ȡ
X=[];
try                                     %��ֹ�����ļ���ȡʧ��
for n=1:File_number
File=[num2str(n),'.wav'];               %�����ļ�����
[x,Fs]=audioread([Path_data,File]);     %������ȡ
X=[X;x(Fs*data_deal.start+1:end,1)];    %��ȡ������,��ȥ��ǰ1s������
end
%% ����Ԥ�����ز���
if Fs~=data_deal.Fs                 %�ж��Ƿ���Ҫ�ز���
    X=resample(X,data_deal.Fs,Fs);  %�ز���
    Fs=data_deal.Fs;                %����Ƶ�ʸ���
end
T=1/Fs;                             %��������
N_amount=length(X);                 %�ź�����
%% ����Ԥ����Ԥ����(�˵���Ƶ�����Ӹ�Ƶ)
X1=filter([1 data_deal.Filter.a],1,X);          %ͨ��һ��һ�׸�ͨ�˲��������˲���Ԥ���أ�
%% ����Ԥ�����ֶ�(�Ӵ�)
N_step=data_deal.Windowing.step/(T*1000);               %����֡��λ��
N_frame=data_deal.Windowing.framelength/(T*1000);       %����λ��
if strcmp(data_deal.Windowing.window,'Hamming')         %�ж��Ƿ��Ǻ�����
    window=hamming(N_frame);                            %�õ�������
end
frame_amount=floor((N_amount-N_frame)/N_step);          %֡�ĸ���
temp=[1:N_step:N_step*frame_amount];                    %��Ƶ����ʼ����
X2=zeros(frame_amount,N_frame);                         %�ֶμӴ��źų�ʼ��
X3=zeros(frame_amount,N_frame);                         %�ֶ��źų�ʼ��
for i=1:frame_amount
    X2(i,:)=(X1(temp(i):temp(i)+N_frame-1).*window)';   %�ֶμӴ�
    X3(i,:)=X(temp(i):temp(i)+N_frame-1)';              %�ֶΣ���Ƶ��ȡʹ�ã�
    E(i)=norm(X2(i,:));                                 %��ʱ��������
end
%% ����Ԥ���������б�
ns_amount=0;                                %��ʼ�������Ķ�������
i=1;
while i<frame_amount
    if E(i)>=data_deal.Silent.E(1)          %�жϵ�ǰ֡�Ƿ����������б�������
       ns_start=i;                          %��¼������ʼλ��
       isns=0;                              %��ʼ�������ж�
       while E(i)>=data_deal.Silent.E(1)    %�жϵ�ǰ֡�Ƿ����������б�������
           i=i+1;
           if E(i)>=data_deal.Silent.E(2)   %�жϵ�ǰ֡�Ƿ����������б������ޣ�����֪����������
               isns=1;                      %�ж�����������
           end
           if i==frame_amount               %��ֹ֡������Χ
               break;
           end
       end
       if isns==1
           ns_amount=ns_amount+1;           %������������
           ns(ns_amount,:)=[ns_start,i-1];  %��������ʼĩλ�ü�¼
       end
    end
    i=i+1;
end
X4=[];X5=[];
for i=1:ns_amount
    X4=[X4;X2(ns(i,1):ns(i,2),:)];          %�ֶμӴ���ȥ��������
    X5=[X5;X3(ns(i,1):ns(i,2),:)];          %�ֶΣ���Ƶ��ȡʹ�ã���ȥ��������
end
new_frame_amount =size(X4,1);       %������֡��
if new_frame_amount>frame_amount/5  %�������ֳ��ȼ��
frame_amount=new_frame_amount;      %֡������
%% ����Ԥ������Ƶ��ȡ
R=AutoCorrelationCal(X5);           %��ʱ����أ�C++���٣�
for i=1:frame_amount
    pitch_T(i)=find_maxn(R(i,:));   %�ҵ���������
end
%% ����Ԥ����ȥ����ƵҰ��
aver=mean(pitch_T);                                         %�õ���������ƽ��ֵ
index=find(abs((pitch_T-aver))>aver/5);                     %�ҵ���Ұ�㣨��ƽ��ֵ������
pitch_T(index)=aver;                                        %ȥ����Ұ���Ӱ��
len=frame_amount-length(index);
for n=1:frame_amount                                        %ת���ɻ�Ƶ
    if(pitch_T(n)==0)                                       %��ֹ����Ϊ0��ʱ��Ƶ��Ϊ�����
        pitch(n)=0;                                         %����Ϊ0��ʱ��Ƶ��ǿ����Ϊ0
    else
        pitch(n)=Fs/pitch_T(n);                             %����תΪƵ��
    end
end
%% ������ȡ
feature=feature_extraction(pitch,pitch_T,X4); %������ȡ
%% ���
[isill,UPDRS]=diagnose(feature);                    %��ϣ��Ƿ񻼲�+UPDRS��
output=[isill,UPDRS,feature];                       %����ϲ����Ƿ񻼲�+UPDRS+������
output=mat2cell(output,1,ones(length(output),1));   %�����ʽ����Ϊcell�����������Python�Ľӿ�
%% ���ⷵ��
else
    output={-1};                    %�������ֹ��������ܼ��
end 
catch
    output={-2};                    %�����ļ���ȡʧ��
end
end
