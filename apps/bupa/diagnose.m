function [ isill , UPDRS ] = diagnose ( feature  )
load model.mat
load z_score.mat
feature=(feature-z_score(1,:))./z_score(2,:);
[isill,t1,t2]=libsvmpredict(0,feature,model.classify,'-q');  %·ÖÀà
[UPDRS,t1,t2]=libsvmpredict(0,feature,model.regress,'-q');   %»Ø¹é
if UPDRS>=200
    UPDRS=200;
elseif UPDRS<=0;
    UPDRS=0;
end
end
