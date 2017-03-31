function [ feature ] = feature_extraction ( pitch , pitch_T , X2 )
N=length(pitch);
%% 基频特征 Pitch
Fo=mean(pitch); %基频的平均值
Fhi=max(pitch); %基频的最大值
Flo=min(pitch); %基频的最小值
Fosd=std(pitch);%基频的标准差
%% 基频扰动 Jitter
Fo_T=mean(pitch_T);                                     %基音周期的平均值
Jitter_abs=mean(abs(pitch_T(2:end)-pitch_T(1:end-1)));  %基音周期绝对扰动
Jitter=Jitter_abs/Fo_T;                                 %基音周期相对扰动
for i=3:N-2
    temp0(i-2)=0.8*pitch_T(i)-0.2*pitch_T(i-2)-0.2*pitch_T(i-2)-0.2*pitch_T(i+1)-0.2*pitch_T(i+2);
end
for i=2:N-1
    temp1(i-1)=2/3*pitch_T(i)-1/3*(pitch_T(i-1)+pitch_T(i+1));
    temp2(i-1)=pitch_T(i+1)-pitch_T(i)-pitch_T(i)+pitch_T(i-1);
end
Jitter_PPQ5=mean(abs(temp0))/Fo_T;                      %基音周期相邻5点
Jitter_rap=mean(abs(temp1))/Fo_T;                       %基音周期相邻3点
Jitter_ddp=mean(abs(temp2))/Fo_T;                       %基音周期相邻3点之差
%% 振幅扰动 shimmer
A=max(X2,[],2)-min(X2,[],2);                            %振幅
Ao=mean(A);                                             %平均振幅
shimmer=mean(abs(A(2:end)-A(1:end-1)))/Ao;              %振幅扰动(%)
shimmer_dB=mean(20*log10(A(1:end-1)./A(2:end)));        %振幅扰动(分贝)
for i=3:N-2
    temp0(i-2)=0.8*A(i)-0.2*A(i-2)-0.2*A(i-2)-0.2*A(i+1)-0.2*A(i+2);
end
for i=2:N-1
    temp1(i-1)=2/3*A(i)-1/3*(A(i-1)+A(i+1));
    temp2(i-1)=A(i+1)-A(i)-A(i)+A(i-1);  
end
for i=6:N-5
    temp3(i-5)=A(i)-1/11*(A(i-5)+A(i-4)+A(i-3)+A(i-2)+A(i-1)+A(i)+A(i+1)+A(i+2)+A(i+3)+A(i+4)+A(i+5));
end
shimmer_APQ5=mean(abs(temp0))/Ao;                       %振幅相邻5点
shimmer_APQ3=mean(abs(temp1))/Ao;                       %振幅相邻3点
shimmer_dda=mean(abs(temp2))/Ao;                        %振幅相邻3点之差
shimmer_APQ11=mean(abs(temp3))/Ao;                      %振幅相邻11点
%% 调和特征
%% 特征合并 
feature=[Fo,Fhi,Flo,Fosd,Jitter,Jitter_abs,Jitter_rap,Jitter_PPQ5,Jitter_ddp,shimmer,shimmer_dB,shimmer_APQ3,shimmer_APQ5,shimmer_APQ11,shimmer_dda];