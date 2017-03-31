#include "mex.h"
void mexFunction(int nlhs, mxArray *plhs[], int nrhs, const mxArray *prhs[])
{
	double *p,*M,*R;
	int Input_Rows, Input_Cols;
	M=mxGetPr(prhs[0]);
	Input_Rows = mxGetM(prhs[0]);
	Input_Cols = mxGetN(prhs[0]);	
	plhs[0] = mxCreateDoubleMatrix(Input_Rows,Input_Cols-1,mxREAL);
	R=(double *)mxGetData(plhs[0]);
	for(int i=0;i<Input_Rows;i++)
	{
		for(int j=0;j<Input_Cols-1;j++)		
		for(int	m=0;m<Input_Cols-j-1;m++)
			*(R+(Input_Rows)*j+i)=*(R+(Input_Rows)*j+i)+(*(M+(Input_Rows)*m+i))*(*(M+(Input_Rows)*(m+j+1)+i));		
	}
}
