function [ feature ] = feature_extraction ( pitch , pitch_T , X2 )
N=length(pitch);
%% ��Ƶ���� Pitch
Fo=mean(pitch); %��Ƶ��ƽ��ֵ
Fhi=max(pitch); %��Ƶ�����ֵ
Flo=min(pitch); %��Ƶ����Сֵ
Fosd=std(pitch);%��Ƶ�ı�׼��
%% ��Ƶ�Ŷ� Jitter
Fo_T=mean(pitch_T);                                     %�������ڵ�ƽ��ֵ
Jitter_abs=mean(abs(pitch_T(2:end)-pitch_T(1:end-1)));  %�������ھ����Ŷ�
Jitter=Jitter_abs/Fo_T;                                 %������������Ŷ�
for i=3:N-2
    temp0(i-2)=0.8*pitch_T(i)-0.2*pitch_T(i-2)-0.2*pitch_T(i-2)-0.2*pitch_T(i+1)-0.2*pitch_T(i+2);
end
for i=2:N-1
    temp1(i-1)=2/3*pitch_T(i)-1/3*(pitch_T(i-1)+pitch_T(i+1));
    temp2(i-1)=pitch_T(i+1)-pitch_T(i)-pitch_T(i)+pitch_T(i-1);
end
Jitter_PPQ5=mean(abs(temp0))/Fo_T;                      %������������5��
Jitter_rap=mean(abs(temp1))/Fo_T;                       %������������3��
Jitter_ddp=mean(abs(temp2))/Fo_T;                       %������������3��֮��
%% ����Ŷ� shimmer
A=max(X2,[],2)-min(X2,[],2);                            %���
Ao=mean(A);                                             %ƽ�����
shimmer=mean(abs(A(2:end)-A(1:end-1)))/Ao;              %����Ŷ�(%)
shimmer_dB=mean(20*log10(A(1:end-1)./A(2:end)));        %����Ŷ�(�ֱ�)
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
shimmer_APQ5=mean(abs(temp0))/Ao;                       %�������5��
shimmer_APQ3=mean(abs(temp1))/Ao;                       %�������3��
shimmer_dda=mean(abs(temp2))/Ao;                        %�������3��֮��
shimmer_APQ11=mean(abs(temp3))/Ao;                      %�������11��
%% ��������
%% �����ϲ� 
feature=[Fo,Fhi,Flo,Fosd,Jitter,Jitter_abs,Jitter_rap,Jitter_PPQ5,Jitter_ddp,shimmer,shimmer_dB,shimmer_APQ3,shimmer_APQ5,shimmer_APQ11,shimmer_dda];