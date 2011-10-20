
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<HEAD>
<META NAME="ROBOTS" CONTENT="NOINDEX, NOFOLLOW">
<title>
行政院衛生署嘉義醫院－網路掛號功能總表
</title>

<meta http-equiv="Content-Type" content="text/html; charset=big5" >
<style> <!-- a:link  {text-decoration: none;} a:visited {text-decoration: none;} --> </style>
<link href="lib/netreg.css" rel="stylesheet" type="text/css">

</HEAD>
<Script LANGUAGE='JavaScript'>

</Script>
<body TOPMARGIN="0" LEFTMARGIN="0" MARGINHEIGHT="0" MARGINWIDTH="0" ONDRAGSTART="window.event.returnValue=false"   onSelectStart="event.returnValue=true"
  >
<TABLE border=0 width="100%"  class='headTitle' summary="版型表格">
<TR><TD width="60%" class='headTitle'>

	<A style="color: #000000; text-decoration: none" HREF="./" title='網路掛號功能總表'>
		行政院衛生署嘉義醫院網路掛號功能總表
		</A>
	<a href="sitemap.asp" accesskey="1" title="上方主選單連結區" style="color: #99CCFF; text-decoration: none">:::</a>
	    </TD>
	    <TD align=left class='smallfont'>您是第&nbsp;<A align="center"><img src='images/left.gif' align='absmiddle' alt=''><img src='images/1.gif' align='absmiddle' alt='1'><img src='images/6.gif' align='absmiddle' alt='6'><img src='images/2.gif' align='absmiddle' alt='2'><img src='images/5.gif' align='absmiddle' alt='5'><img src='images/9.gif' align='absmiddle' alt='9'><img src='images/2.gif' align='absmiddle' alt='2'><img src='images/right.gif' align='absmiddle' alt=''><A>&nbsp;位使用者</TD>
	</TR>
	</TABLE>
<table border="0" cellpadding="0" cellspacing="1" width="100%" summary="選單功能版型表格">
  <TR>
    <TD width="100%" class='headMenu' VALIGN="middle" NOWRAP>
	&nbsp;
	<A HREF='./QryTable.asp' title='門診表'>
	門診表</A>&nbsp;|
	
		&nbsp;<A HREF='./ChooseDep.asp' title='初診預約掛號'>初診預約掛號</A>&nbsp;|
	
	&nbsp;<A HREF='./regreq.asp' title='掛號查詢'>掛號查詢</A>&nbsp;|
	&nbsp;<A HREF='./QryNum.asp' title='診間看診號查詢'>診間看診號查詢</A>&nbsp;|
	&nbsp;<A HREF='http://www.chyi.doh.gov.tw'  TArget='_top' title='開新視窗到醫院首頁'>行政院衛生署嘉義醫院首頁	</A>&nbsp;|
	
	&nbsp;<A HREF='netreg.asp?mode=E' title='English'>English</A>&nbsp;|
 		&nbsp;<A HREF='sitemap.asp' title='網站導覽'>網站導覽</A>&nbsp;|
    </TD>  
  </TR>  
  <TR>
    <TD width='100%' class='headMenu' VALIGN='middle' NOWRAP>
	&nbsp;<A HREF='./ChooseDep.asp?subseq=Y' title='複診預約掛號'>複診預約掛號
	</A>&nbsp;|
	&nbsp;<A HREF='./regcan.asp' title='掛號取消'>掛號取消
	</A>&nbsp;|

    </TD>  
  </TR>  
</table>  
</body>
<!---------------94.04.17防駭用加解密Chris------------------------------------>
<!----------------96.04.16防駭用加解密和轉檔程式Chris------------------------->

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
		{	alert("請輸入身份證字號或病歷號碼");		}

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
		{	alert("請輸入生日");
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
  <P>本網頁使用Script 主要在審核必要欄位輸入，但是您的瀏覽器並不支援，所以請自行審核你的欄位資料皆輸入。如:身份證字號或病歷號碼</P>
 </NOSCRIPT>

<a href='sitemap.asp' accesskey='C' title='內容顯示區' style='color: #FFFFFF; text-decoration: none'>:::</a><br><FORM METHOD='POST' ACTION='PatReg.asp' name='RegFrm' onsubmit='return datacheck()'><input type='hidden' name=RandNumb_D value=JMHNGMGPRPHRIPQPQMD5><input type='hidden' name=mode value=><input type='hidden' name=area value=1><input type='hidden' name=areaid value=><input type='hidden' name=opcode value=DQ><FONT class='transName'><H2>取消預約掛號選單</H2></font>	1.請先輸入 <FONT class='inputID'><LABEL for='idno'>身份證字號</LABEL></FONT><INPUT accesskey='I' NAME='idno' SIZE=11 MAXLENGTH=10 OnKeyPress='enterSend()'   value=''>(10位)&nbsp;或 <FONT class='inputID'><LABEL for='Patid'>病歷號碼</LABEL></FONT><INPUT id='Patid' NAME='Patid' SIZE=11 MAXLENGTH=8 OnKeyPress='enterSend()'>(8位):<BR><BR>	2.<LEGEND>國別</LEGEND>：<INPUT id='origid0' name=origid type=radio value='1' checked><LABEL for='origid0'>本國</LABEL>	   <INPUT id='origid1' name=origid type=radio value='2'><LABEL for='origid1'>外國</LABEL>	<BR><BR>3.生日:民國<SELECT id='BirthY' name='BirthY'> <OPTION selected></OPTION>
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
</SELECT>年<SELECT id=BirthM name=BirthM ><OPTION selected></OPTION>
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
</SELECT>月<SELECT id=BirthD name=BirthD><OPTION selected></OPTION>
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
</SELECT>日<input name='NeedBirth' value='Y' type='hidden'><BR><BR><INPUT accesskey='S' TYPE='submit' VALUE='完成,送出' id=button1 name=button1>&nbsp;<input TYPE='reset' VALUE='清除,重新輸入'>
</p>
</form>

<Script>
SetFocus();
</Script>
<NOSCRIPT>本網頁使用Script但是您的瀏覽器並不支援, 目的是在設定初始位置</NOSCRIPT>
<body onmouseover="window.status=''" onmouseout="window.status=''" onmousedown="window.status=''" onmousemove="window.status=''" onfocus="window.status=''" onblur="window.status=''" oncontextmenu='window.event.returnValue=false'>
<HR>
<div><center>
<span class="smallfont">
院址：嘉義市北港路312號。電話：(05)2319090。傳真：(05)2316781。
<br>
	本網路掛號網頁由大同世界科技公司開發。
			 <H2><br> <FONT SIZE=5 COLOR="#FF0000">   網路初診預約掛號患者請於</FONT><br>
		 <br> <FONT SIZE=5 COLOR="#FF0000">  上午：11：30  前  先至掛號櫃檯報到 </FONT><br> 
		  <br> <FONT SIZE=5 COLOR="#FF0000"> 下午：16：00  前  先至掛號櫃檯報到  </FONT> <br> 
		   <br> <FONT SIZE=5 COLOR="#FF0000"> 晚上：20：20  前  先至掛號櫃檯報到 </FONT> <br>  <H2> 
		  
			
		

</span>
</center></div>
 </BODY>
</HTML>

<!---------------96.04.11防駭用Chris------------------------------------------>
<script language="JavaScript">
var txt = "歡迎使用網路掛號系統，祝您有個愉快的一天!!";
function flush(){
 window.status = txt;
 timerID = setTimeout("flush()",0); }
flush();
</script>
<!---------------------------------------------------------------------------->