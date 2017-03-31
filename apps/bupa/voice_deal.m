function [ output ] = voice_deal ( Path_data , File_number )
%% 参数设计
data_deal.Fs=10000;                     %数据重采样频率（语音信号范围为300~3400HZ）
data_deal.FFT.N=0;                      %傅立叶的N值（填0的话就使用默认信号长度）
data_deal.Filter.a=-0.9375;             %高通滤波器的预加重系数
data_deal.start=1;                      %开始读取（从1s后）
data_deal.Windowing.window='Hamming';   %加窗的类型:'Hamming':汉明窗
data_deal.Windowing.step=10;            %窗的帧移（单位/ms）
data_deal.Windowing.framelength=25;     %窗的时间长度（单位/ms）
data_deal.Silent.E=[0.02,0.05];         %无声检测门限（低门限和高门限）
%% 数据读取
X=[];
try                                     %防止语音文件读取失败
for n=1:File_number
File=[num2str(n),'.wav'];               %数据文件名称
[x,Fs]=audioread([Path_data,File]);     %语音读取
X=[X;x(Fs*data_deal.start+1:end,1)];    %提取左声道,并去除前1s的声音
end
%% 语音预处理：重采样
if Fs~=data_deal.Fs                 %判断是否需要重采样
    X=resample(X,data_deal.Fs,Fs);  %重采样
    Fs=data_deal.Fs;                %采样频率更新
end
T=1/Fs;                             %采样周期
N_amount=length(X);                 %信号数量
%% 语音预处理：预加重(滤掉低频，增加高频)
X1=filter([1 data_deal.Filter.a],1,X);          %通过一个一阶高通滤波器进行滤波（预加重）
%% 语音预处理：分段(加窗)
N_step=data_deal.Windowing.step/(T*1000);               %窗的帧移位数
N_frame=data_deal.Windowing.framelength/(T*1000);       %窗的位数
if strcmp(data_deal.Windowing.window,'Hamming')         %判断是否是汉明窗
    window=hamming(N_frame);                            %得到窗函数
end
frame_amount=floor((N_amount-N_frame)/N_step);          %帧的个数
temp=[1:N_step:N_step*frame_amount];                    %分频的起始坐标
X2=zeros(frame_amount,N_frame);                         %分段加窗信号初始化
X3=zeros(frame_amount,N_frame);                         %分段信号初始化
for i=1:frame_amount
    X2(i,:)=(X1(temp(i):temp(i)+N_frame-1).*window)';   %分段加窗
    X3(i,:)=X(temp(i):temp(i)+N_frame-1)';              %分段（基频提取使用）
    E(i)=norm(X2(i,:));                                 %短时能量分析
end
%% 语音预处理：无声判别
ns_amount=0;                                %初始化有声的段落数量
i=1;
while i<frame_amount
    if E(i)>=data_deal.Silent.E(1)          %判断当前帧是否满足无声判别下门限
       ns_start=i;                          %记录段落起始位置
       isns=0;                              %初始化语音判断
       while E(i)>=data_deal.Silent.E(1)    %判断当前帧是否满足无声判别下门限
           i=i+1;
           if E(i)>=data_deal.Silent.E(2)   %判断当前帧是否满足无声判别上门限（即可知不是噪音）
               isns=1;                      %判断是有声段落
           end
           if i==frame_amount               %防止帧超出范围
               break;
           end
       end
       if isns==1
           ns_amount=ns_amount+1;           %有声段落数量
           ns(ns_amount,:)=[ns_start,i-1];  %有声段落始末位置记录
       end
    end
    i=i+1;
end
X4=[];X5=[];
for i=1:ns_amount
    X4=[X4;X2(ns(i,1):ns(i,2),:)];          %分段加窗（去掉无声）
    X5=[X5;X3(ns(i,1):ns(i,2),:)];          %分段（基频提取使用）（去掉无声）
end
new_frame_amount =size(X4,1);       %有声的帧数
if new_frame_amount>frame_amount/5  %无声部分长度检测
frame_amount=new_frame_amount;      %帧数更新
%% 语音预处理：基频提取
R=AutoCorrelationCal(X5);           %短时自相关（C++加速）
for i=1:frame_amount
    pitch_T(i)=find_maxn(R(i,:));   %找到基音周期
end
%% 语音预处理：去除基频野点
aver=mean(pitch_T);                                         %得到基音周期平均值
index=find(abs((pitch_T-aver))>aver/5);                     %找到大野点（与平均值相差过大）
pitch_T(index)=aver;                                        %去除大野点的影响
len=frame_amount-length(index);
for n=1:frame_amount                                        %转换成基频
    if(pitch_T(n)==0)                                       %防止周期为0的时候，频率为无穷大
        pitch(n)=0;                                         %周期为0的时候，频率强行置为0
    else
        pitch(n)=Fs/pitch_T(n);                             %周期转为频率
    end
end
%% 特征提取
feature=feature_extraction(pitch,pitch_T,X4); %特征提取
%% 诊断
[isill,UPDRS]=diagnose(feature);                    %诊断（是否患病+UPDRS）
output=[isill,UPDRS,feature];                       %输出合并（是否患病+UPDRS+特征）
output=mat2cell(output,1,ones(length(output),1));   %输出格式更改为cell，便于输出给Python的接口
%% 问题返回
else
    output={-1};                    %无声部分过长，不能检测
end 
catch
    output={-2};                    %语音文件读取失败
end
end
