
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<HEAD>
<META NAME="ROBOTS" CONTENT="NOINDEX, NOFOLLOW">
<title>
��F�|�å͸p�Ÿq��|�к��������\���`��
</title>

<meta http-equiv="Content-Type" content="text/html; charset=big5" >
<style> <!-- a:link  {text-decoration: none;} a:visited {text-decoration: none;} --> </style>
<link href="lib/netreg.css" rel="stylesheet" type="text/css">

</HEAD>
<Script LANGUAGE='JavaScript'>

</Script>
<body TOPMARGIN="0" LEFTMARGIN="0" MARGINHEIGHT="0" MARGINWIDTH="0" ONDRAGSTART="window.event.returnValue=false"   onSelectStart="event.returnValue=true"
  >
<TABLE border=0 width="100%"  class='headTitle' summary="�������">
<TR><TD width="60%" class='headTitle'>

	<A style="color: #000000; text-decoration: none" HREF="./" title='���������\���`��'>
		��F�|�å͸p�Ÿq��|���������\���`��
		</A>
	<a href="sitemap.asp" accesskey="1" title="�W��D���s����" style="color: #99CCFF; text-decoration: none">:::</a>
	    </TD>
	    <TD align=left class='smallfont'>�z�O��&nbsp;<A align="center"><img src='images/left.gif' align='absmiddle' alt=''><img src='images/1.gif' align='absmiddle' alt='1'><img src='images/6.gif' align='absmiddle' alt='6'><img src='images/2.gif' align='absmiddle' alt='2'><img src='images/5.gif' align='absmiddle' alt='5'><img src='images/9.gif' align='absmiddle' alt='9'><img src='images/2.gif' align='absmiddle' alt='2'><img src='images/right.gif' align='absmiddle' alt=''><A>&nbsp;��ϥΪ�</TD>
	</TR>
	</TABLE>
<table border="0" cellpadding="0" cellspacing="1" width="100%" summary="���\�઩�����">
  <TR>
    <TD width="100%" class='headMenu' VALIGN="middle" NOWRAP>
	&nbsp;
	<A HREF='./QryTable.asp' title='���E��'>
	���E��</A>&nbsp;|
	
		&nbsp;<A HREF='./ChooseDep.asp' title='��E�w������'>��E�w������</A>&nbsp;|
	
	&nbsp;<A HREF='./regreq.asp' title='�����d��'>�����d��</A>&nbsp;|
	&nbsp;<A HREF='./QryNum.asp' title='�E���ݶE���d��'>�E���ݶE���d��</A>&nbsp;|
	&nbsp;<A HREF='http://www.chyi.doh.gov.tw'  TArget='_top' title='�}�s��������|����'>��F�|�å͸p�Ÿq��|����	</A>&nbsp;|
	
	&nbsp;<A HREF='netreg.asp?mode=E' title='English'>English</A>&nbsp;|
 		&nbsp;<A HREF='sitemap.asp' title='��������'>��������</A>&nbsp;|
    </TD>  
  </TR>  
  <TR>
    <TD width='100%' class='headMenu' VALIGN='middle' NOWRAP>
	&nbsp;<A HREF='./ChooseDep.asp?subseq=Y' title='�ƶE�w������'>�ƶE�w������
	</A>&nbsp;|
	&nbsp;<A HREF='./regcan.asp' title='��������'>��������
	</A>&nbsp;|

    </TD>  
  </TR>  
</table>  
</body>
<!---------------94.04.17���b�Υ[�ѱKChris------------------------------------>
<!----------------96.04.16���b�Υ[�ѱK�M���ɵ{��Chris------------------------->

<Script LANGUAGE='JavaScript'>
<!--
function datacheck() {	
	var p=document.RegFrm.Patid.value
	var idno=document.RegFrm.idno.value
	var mode = document.RegFrm.mode.value ;
	var NeedBirth = document.RegFrm.NeedBirth.value;
	var flagY = false;
	var flagM = false;
	var flagD = false;

	if ( (p.length == 0) && (idno.length == 0)) {
		if ( mode == "E" ) 
		{	alert("Please input ID NO. or Medical Record NO.");	}
		else
		{	alert("�п�J�����Ҧr���ίf�����X");		}

		document.RegFrm.idno.focus();	
	}
	else if (NeedBirth == "Y") {

		for ( i = 0 ; i < document.RegFrm.BirthY.length ; i++){
			if (document.RegFrm.BirthY.options[i].selected )
			{	if (document.RegFrm.BirthY.options[i].value != "") flagY = true;		}
		}
		for ( i = 0 ; i < document.RegFrm.BirthM.length ; i++){
			if (document.RegFrm.BirthM.options[i].selected )
			{	if (document.RegFrm.BirthM.options[i].value != "") flagM = true;		}
		}
		for ( i = 0 ; i < document.RegFrm.BirthD.length ; i++){
			if (document.RegFrm.BirthD.options[i].selected )
			{	if (document.RegFrm.BirthD.options[i].value != "") flagD = true;		}	}
		if (!(flagY && flagM && flagD))
		{	alert("�п�J�ͤ�");
			return false;
		}
	}
	else  {
		document.RegFrm.submit();
	}
}

function SetFocus() {
	document.RegFrm.idno.focus();
}
function enterSend() {
		if( event.keyCode == 13 ) {
			datacheck ();
		}
	}
-->
</Script>
<NOSCRIPT>
  <P>�������ϥ�Script �D�n�b�f�֥��n����J�A���O�z���s�����ä��䴩�A�ҥH�Цۦ�f�֧A������Ƭҿ�J�C�p:�����Ҧr���ίf�����X</P>
 </NOSCRIPT>

<a href='sitemap.asp' accesskey='C' title='���e��ܰ�' style='color: #FFFFFF; text-decoration: none'>:::</a><br><FORM METHOD='POST' ACTION='PatReg.asp' name='RegFrm' onsubmit='return datacheck()'><input type='hidden' name=RandNumb_D value=JMHNGMGPRPHRIPQPQMD5><input type='hidden' name=mode value=><input type='hidden' name=area value=1><input type='hidden' name=areaid value=><input type='hidden' name=opcode value=DQ><FONT class='transName'><H2>�����w���������</H2></font>	1.�Х���J <FONT class='inputID'><LABEL for='idno'>�����Ҧr��</LABEL></FONT><INPUT accesskey='I' NAME='idno' SIZE=11 MAXLENGTH=10 OnKeyPress='enterSend()'   value=''>(10��)&nbsp;�� <FONT class='inputID'><LABEL for='Patid'>�f�����X</LABEL></FONT><INPUT id='Patid' NAME='Patid' SIZE=11 MAXLENGTH=8 OnKeyPress='enterSend()'>(8��):<BR><BR>	2.<LEGEND>��O</LEGEND>�G<INPUT id='origid0' name=origid type=radio value='1' checked><LABEL for='origid0'>����</LABEL>	   <INPUT id='origid1' name=origid type=radio value='2'><LABEL for='origid1'>�~��</LABEL>	<BR><BR>3.�ͤ�:����<SELECT id='BirthY' name='BirthY'> <OPTION selected></OPTION>
<OPTION value='-10' >-10</OPTION>
<OPTION value='-9' >-9</OPTION>
<OPTION value='-8' >-8</OPTION>
<OPTION value='-7' >-7</OPTION>
<OPTION value='-6' >-6</OPTION>
<OPTION value='-5' >-5</OPTION>
<OPTION value='-4' >-4</OPTION>
<OPTION value='-3' >-3</OPTION>
<OPTION value='-2' >-2</OPTION>
<OPTION value='-1' >-1</OPTION>
<OPTION value='1' >1</OPTION>
<OPTION value='2' >2</OPTION>
<OPTION value='3' >3</OPTION>
<OPTION value='4' >4</OPTION>
<OPTION value='5' >5</OPTION>
<OPTION value='6' >6</OPTION>
<OPTION value='7' >7</OPTION>
<OPTION value='8' >8</OPTION>
<OPTION value='9' >9</OPTION>
<OPTION value='10' >10</OPTION>
<OPTION value='11' >11</OPTION>
<OPTION value='12' >12</OPTION>
<OPTION value='13' >13</OPTION>
<OPTION value='14' >14</OPTION>
<OPTION value='15' >15</OPTION>
<OPTION value='16' >16</OPTION>
<OPTION value='17' >17</OPTION>
<OPTION value='18' >18</OPTION>
<OPTION value='19' >19</OPTION>
<OPTION value='20' >20</OPTION>
<OPTION value='21' >21</OPTION>
<OPTION value='22' >22</OPTION>
<OPTION value='23' >23</OPTION>
<OPTION value='24' >24</OPTION>
<OPTION value='25' >25</OPTION>
<OPTION value='26' >26</OPTION>
<OPTION value='27' >27</OPTION>
<OPTION value='28' >28</OPTION>
<OPTION value='29' >29</OPTION>
<OPTION value='30' >30</OPTION>
<OPTION value='31' >31</OPTION>
<OPTION value='32' >32</OPTION>
<OPTION value='33' >33</OPTION>
<OPTION value='34' >34</OPTION>
<OPTION value='35' >35</OPTION>
<OPTION value='36' >36</OPTION>
<OPTION value='37' >37</OPTION>
<OPTION value='38' >38</OPTION>
<OPTION value='39' >39</OPTION>
<OPTION value='40' >40</OPTION>
<OPTION value='41' >41</OPTION>
<OPTION value='42' >42</OPTION>
<OPTION value='43' >43</OPTION>
<OPTION value='44' >44</OPTION>
<OPTION value='45' >45</OPTION>
<OPTION value='46' >46</OPTION>
<OPTION value='47' >47</OPTION>
<OPTION value='48' >48</OPTION>
<OPTION value='49' >49</OPTION>
<OPTION value='50' >50</OPTION>
<OPTION value='51' >51</OPTION>
<OPTION value='52' >52</OPTION>
<OPTION value='53' >53</OPTION>
<OPTION value='54' >54</OPTION>
<OPTION value='55' >55</OPTION>
<OPTION value='56' >56</OPTION>
<OPTION value='57' >57</OPTION>
<OPTION value='58' >58</OPTION>
<OPTION value='59' >59</OPTION>
<OPTION value='60' >60</OPTION>
<OPTION value='61' >61</OPTION>
<OPTION value='62' >62</OPTION>
<OPTION value='63' >63</OPTION>
<OPTION value='64' >64</OPTION>
<OPTION value='65' >65</OPTION>
<OPTION value='66' >66</OPTION>
<OPTION value='67' >67</OPTION>
<OPTION value='68' >68</OPTION>
<OPTION value='69' >69</OPTION>
<OPTION value='70' >70</OPTION>
<OPTION value='71' >71</OPTION>
<OPTION value='72' >72</OPTION>
<OPTION value='73' >73</OPTION>
<OPTION value='74' >74</OPTION>
<OPTION value='75' >75</OPTION>
<OPTION value='76' >76</OPTION>
<OPTION value='77' >77</OPTION>
<OPTION value='78' >78</OPTION>
<OPTION value='79' >79</OPTION>
<OPTION value='80'  selected >80</OPTION>
<OPTION value='81' >81</OPTION>
<OPTION value='82' >82</OPTION>
<OPTION value='83' >83</OPTION>
<OPTION value='84' >84</OPTION>
<OPTION value='85' >85</OPTION>
<OPTION value='86' >86</OPTION>
<OPTION value='87' >87</OPTION>
<OPTION value='88' >88</OPTION>
<OPTION value='89' >89</OPTION>
<OPTION value='90' >90</OPTION>
<OPTION value='91' >91</OPTION>
<OPTION value='92' >92</OPTION>
<OPTION value='93' >93</OPTION>
<OPTION value='94' >94</OPTION>
<OPTION value='95' >95</OPTION>
<OPTION value='96' >96</OPTION>
<OPTION value='97' >97</OPTION>
<OPTION value='98' >98</OPTION>
<OPTION value='99' >99</OPTION>
<OPTION value='100' >100</OPTION>
</SELECT>�~<SELECT id=BirthM name=BirthM ><OPTION selected></OPTION>
<OPTION value='1'>1</OPTION>
<OPTION value='2'>2</OPTION>
<OPTION value='3'>3</OPTION>
<OPTION value='4'>4</OPTION>
<OPTION value='5'>5</OPTION>
<OPTION value='6'>6</OPTION>
<OPTION value='7'>7</OPTION>
<OPTION value='8'>8</OPTION>
<OPTION value='9'>9</OPTION>
<OPTION value='10'>10</OPTION>
<OPTION value='11'>11</OPTION>
<OPTION value='12'>12</OPTION>
</SELECT>��<SELECT id=BirthD name=BirthD><OPTION selected></OPTION>
<OPTION value='1'>1</OPTION>
<OPTION value='2'>2</OPTION>
<OPTION value='3'>3</OPTION>
<OPTION value='4'>4</OPTION>
<OPTION value='5'>5</OPTION>
<OPTION value='6'>6</OPTION>
<OPTION value='7'>7</OPTION>
<OPTION value='8'>8</OPTION>
<OPTION value='9'>9</OPTION>
<OPTION value='10'>10</OPTION>
<OPTION value='11'>11</OPTION>
<OPTION value='12'>12</OPTION>
<OPTION value='13'>13</OPTION>
<OPTION value='14'>14</OPTION>
<OPTION value='15'>15</OPTION>
<OPTION value='16'>16</OPTION>
<OPTION value='17'>17</OPTION>
<OPTION value='18'>18</OPTION>
<OPTION value='19'>19</OPTION>
<OPTION value='20'>20</OPTION>
<OPTION value='21'>21</OPTION>
<OPTION value='22'>22</OPTION>
<OPTION value='23'>23</OPTION>
<OPTION value='24'>24</OPTION>
<OPTION value='25'>25</OPTION>
<OPTION value='26'>26</OPTION>
<OPTION value='27'>27</OPTION>
<OPTION value='28'>28</OPTION>
<OPTION value='29'>29</OPTION>
<OPTION value='30'>30</OPTION>
<OPTION value='31'>31</OPTION>
</SELECT>��<input name='NeedBirth' value='Y' type='hidden'><BR><BR><INPUT accesskey='S' TYPE='submit' VALUE='����,�e�X' id=button1 name=button1>&nbsp;<input TYPE='reset' VALUE='�M��,���s��J'>
</p>
</form>

<Script>
SetFocus();
</Script>
<NOSCRIPT>�������ϥ�Script���O�z���s�����ä��䴩, �ت��O�b�]�w��l��m</NOSCRIPT>
<body onmouseover="window.status=''" onmouseout="window.status=''" onmousedown="window.status=''" onmousemove="window.status=''" onfocus="window.status=''" onblur="window.status=''" oncontextmenu='window.event.returnValue=false'>
<HR>
<div><center>
<span class="smallfont">
�|�}�G�Ÿq���_���312���C�q�ܡG(05)2319090�C�ǯu�G(05)2316781�C
<br>
	���������������Ѥj�P�@�ɬ�ޤ��q�}�o�C
			 <H2><br> <FONT SIZE=5 COLOR="#FF0000">   ������E�w�������w�̽Щ�</FONT><br>
		 <br> <FONT SIZE=5 COLOR="#FF0000">  �W�ȡG11�G30  �e  ���ܱ����d�i���� </FONT><br> 
		  <br> <FONT SIZE=5 COLOR="#FF0000"> �U�ȡG16�G00  �e  ���ܱ����d�i����  </FONT> <br> 
		   <br> <FONT SIZE=5 COLOR="#FF0000"> �ߤW�G20�G20  �e  ���ܱ����d�i���� </FONT> <br>  <H2> 
		  
			
		

</span>
</center></div>
 </BODY>
</HTML>

<!---------------96.04.11���b��Chris------------------------------------------>
<script language="JavaScript">
var txt = "�w��ϥκ��������t�ΡA���z���Ӵr�֪��@��!!";
function flush(){
 window.status = txt;
 timerID = setTimeout("flush()",0); }
flush();
</script>
<!---------------------------------------------------------------------------->