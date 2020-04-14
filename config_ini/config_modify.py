#usr/env/bin python3
# -*- coding:utf-8 -*-

# import os , random
import io
from IPy import IP

#系统配置项

NODE_NUMBER_FUNCTION	= 3
NODE_NUMBER_FSFB2 		= 3
NODE_NUMBER_RAW 		= 3
NODE_NUMBER_RSSPI 		= 2
NODE_NUMBER_RSSPII		= 3
NODE_NUMBER_REDUN 		= 3
NODE_NUMBER_SDM			= 3

SYSTEM_CYCLE_NUMBER		= 250

#RSSP1配置项
RSSP1_LOCAL_CYCLE		= 250
REMOTE_RSSP1_CYCLE		= 250
RSSP1_LOCAL_NODE		= 0x7001
RSSP1_REMOTE_NODE_INIT	= 0x7101

#RSSP2配置项
RSSP2_LOCAL_CYCLE		= 250
RSSP2_LOCAL_NODE		= 0x6013C01
RSSP2_REMOTE_NODE_INIT	= 0x6023C01

#IP配置项
REMOTE_NET_IP_INIT		= 10
REMOTE_NET_PORT_INIT	= 60010
LOCAL_NET_PORT_INIT		= 50001
LOCAL_NET_IP = \
{
	#配置本地 IP:MASK
	"MNCU1_N1_A":"10.1.2.5:255.255.0.0",		#RSSP1-A-Red
	"MNCU1_N2_A":"10.2.2.5:255.255.0.0",		#RSSP1-A-Blue
	"MNCU1_N1_B":"10.1.2.6:255.255.0.0",		#RSSP1-A-Red
	"MNCU1_N2_B":"10.2.2.6:255.255.0.0",		#RSSP1-A-Blue

	"MNCU1_N3_A":"10.5.1.5:255.255.0.0",		#RSSP1-B-Red
	"MNCU1_N4_A":"10.6.1.5:255.255.0.0",		#RSSP1-B-Blue
	"MNCU1_N3_B":"10.5.1.6:255.255.0.0",		#RSSP1-B-Red
	"MNCU1_N4_B":"10.6.1.6:255.255.0.0",		#RSSP1-B-Blue

	"MCU_N1_A" :"192.100.100.6:255.255.255.0",	#SDM-A/REDUN-A
	"MCU_N1_B" :"192.100.200.6:255.255.255.0",	#SDM-A/RAW-A

	"MCU_N2_A" :"192.100.100.8:255.255.255.0",	#SDM-B/REDUN-B
	"MCU_N2_B" :"192.100.200.8:255.255.255.0"	#SDM-B/RAW-B
}

#节点使用的本地IP
LOCAL_USED_BY_FUNC		= ['MNCU1_N3_A','MNCU1_N3_B','MNCU1_N4_A','MNCU1_N4_B']
LOCAL_USED_BY_FSFB2		= ['MNCU1_N2_A','MNCU1_N2_B']
LOCAL_USED_BY_RSSP1_A	= ['MNCU1_N1_A','MNCU1_N2_A','MNCU1_N1_B','MNCU1_N2_B']
LOCAL_USED_BY_RSSP1_B	= ['MNCU1_N3_A','MNCU1_N4_A','MNCU1_N3_B','MNCU1_N4_B']
LOCAL_USED_BY_RSSP2_A	= ['MNCU1_N1_A','MNCU1_N2_A','MNCU1_N1_B','MNCU1_N2_B']
LOCAL_USED_BY_RSSP2_B	= ['MNCU1_N3_A','MNCU1_N4_A','MNCU1_N3_B','MNCU1_N4_B']
LOCAL_USED_BY_SDM_A		= ['MCU_N1_A','MCU_N1_B']
LOCAL_USED_BY_SDM_B		= ['MCU_N2_A','MCU_N2_B']
LOCAL_USED_BY_REDUN		= ['MNCU1_N4_A','MNCU1_N4_B']
LOCAL_USED_BY_RAW		= ['MNCU1_N3_A','MNCU1_N3_B']

#预定义项
CVC_APP_TYPE_FUNC		= 0
CVC_APP_TYPE_SACEM		= 1
CVC_APP_TYPE_FSFB2		= 2
CVC_APP_TYPE_RAW		= 3
CVC_APP_TYPE_RSSPI		= 4
CVC_APP_TYPE_RSSPII		= 5
CVC_APP_TYPE_SUB037		= 6
CVC_APP_TYPE_RMS_GAPP	= 7
CVC_APP_TYPE_ODOMETER	= 8
CVC_APP_TYPE_IO			= 9
CVC_APP_TYPE_BEACON		= 10
CVC_APP_TYPE_OMAP		= 11
CVC_APP_TYPE_STBY		= 12
CVC_APP_TYPE_SDM		= 13
CVC_APP_TYPE_REDUNDANCY	= 14

#初始设备PID
START_PID_FUNC			= 2001
START_PID_FSFB2			= 1001
START_PID_RAW			= 3001
START_PID_REDUN 		= 4001
START_PID_RSSPI 		= 3401
START_PID_RSSPII		= 6001
START_PID_SDM			= 990


#远端设备名称
REMOTE_NAME = ''

#生成ini文件编码格式
FileEncodeType			= 'utf-8'

#==========================================================
#CreateEquipmentFile
#==========================================================
class Equipment(object):
	'''
	@ equipment.ini配置文件生成
	'''

	CVC_EQU_MSG		= []
	
	'''
	@ 基本元素	 
	..MAP
	PERIPHERAL_ID 
	EQU_TYPE 
	EQU_NODE 
	EQU_IDX 
	EQU_CONNECT 
	..GAPP/MRMS
	SSTYPE_ID 
	SUBLOGIC_ID 
	SUBSYSTEM_ID 
	SSNODE_ID 
	SIG_VER 
	LOCAL_MSGID 
	REMOTE_MSGID 
	..RMS
	RMS_VER 
	RMS_TYPE 
	RMS_SN_INIT 
	RMS_SN_MAX 
	RMS_SN_TABLESIZE 
	'''

	

	def __init__(self, FSFB2_VSN = 1, RSSP1_VSN = 1, RSSP2_VSN = 1):
		self.__total_link_number = 2
		self.__VSN_FSFB2=FSFB2_VSN
		self.__VSN_RSSP1=RSSP1_VSN
		self.__VSN_RSSP2=RSSP2_VSN
		self.__RMS_Idx = 0
		self.__RSSPI_Idx = 0
		self.__RSSPII_Idx = 0

		self.map_fields = {}
		self.map_fields.update(COMMENT=0)
		self.map_fields.update(PERIPHERAL_ID=0)
		self.map_fields.update(EQU_TYPE=0)
		self.map_fields.update(EQU_NODE=0)
		self.map_fields.update(EQU_IDX=0)
		self.map_fields.update(EQU_CONNECT=0)
		self.map_fields.update(SSTYPE_ID=0)
		self.map_fields.update(SUBLOGIC_ID=0)
		self.map_fields.update(SUBSYSTEM_ID=0)
		self.map_fields.update(SSNODE_ID=0)
		self.map_fields.update(SIG_VER=0)
		self.map_fields.update(LOCAL_MSGID=0)
		self.map_fields.update(REMOTE_MSGID=0)
		self.map_fields.update(RMS_VER=0)
		self.map_fields.update(RMS_TYPE=0)
		self.map_fields.update(RMS_SN_INIT=0)
		self.map_fields.update(RMS_SN_MAX=0)
		self.map_fields.update(RMS_SN_TABLESIZE=0)

		#return super().__init__(*args, **kwargs)

	def ResetMapDict(self):
		self.map_fields.update(COMMENT=0)
		self.map_fields.update(PERIPHERAL_ID=0)
		self.map_fields.update(EQU_TYPE=0)
		self.map_fields.update(EQU_NODE=0)
		self.map_fields.update(EQU_IDX=0)
		self.map_fields.update(EQU_CONNECT=0)
		self.map_fields.update(SSTYPE_ID=0)
		self.map_fields.update(SUBLOGIC_ID=0)
		self.map_fields.update(SUBSYSTEM_ID=0)
		self.map_fields.update(SSNODE_ID=0)
		self.map_fields.update(SIG_VER=0)
		self.map_fields.update(LOCAL_MSGID=0)
		self.map_fields.update(REMOTE_MSGID=0)
		self.map_fields.update(RMS_VER=0)
		self.map_fields.update(RMS_TYPE=0)
		self.map_fields.update(RMS_SN_INIT=0)
		self.map_fields.update(RMS_SN_MAX=0)
		self.map_fields.update(RMS_SN_TABLESIZE=0)
		return

	def AddEquipmentGlobalCfg(self):
		'''
		@ 增加全局区字段
		'''
		
		self.CVC_EQU_MSG.insert(0,["[SITES_INFO]","SITE_NO = 51039","SITE_NAME = 合信路站"])
		self.CVC_EQU_MSG.insert(1,[";预留接口，配置应用版本，默认为0.0.0","[APP_VER]",\
								   "SOFTWARE_VERSION = 0.0.0","DATA_VERSION = 0.0.0"])
		self.CVC_EQU_MSG.insert(2,["[CVC_CYCLE]","MAIN_CYCLE = 250"])
		
		
		map_VSN_FSFB2 = "FSFB2 = %d" % self.__VSN_FSFB2
		map_VSN_RSSP1 = "RSSP1 = %d" % self.__VSN_RSSP1
		map_VSN_RSSP2 = "RSSP2 = %d" % self.__VSN_RSSP2
		self.CVC_EQU_MSG.insert(3,["[VSN]",map_VSN_FSFB2,map_VSN_RSSP1,map_VSN_RSSP2])
		
		self.CVC_EQU_MSG.insert(4,["[EQULIST]",";设备数量","DEV_NUM = %d" % self.__total_link_number,\
								   ";本地设备名称","LOCAL_EQU = IXL,SDM",";远端设备名称","REMOTE_EQU = %s" % REMOTE_NAME])
		self.CVC_EQU_MSG.insert(5,["[IXL]","PERIPHERAL_ID = 0","SSTYPE_ID = 60","SUBLOGIC_ID = 2",\
								   "SUBSYSTEM_ID = 2","SSNODE_ID = 15362","RMS_TYPE = 1","RMS_VER = 1"])
		self.CVC_EQU_MSG.insert(6,["[SDM]","PERIPHERAL_ID = 0","SSTYPE_ID = 50","SUBLOGIC_ID = 0",\
								   "SUBSYSTEM_ID = 0","SSNODE_ID = 11","RMS_TYPE = 0","RMS_VER = 0"])
		
		return

	def AddBasicMapCfg(self, desc="None", **kw):
		'''
		@增加各个MAP字段配置
		'''
		map_basic_param = [
			'COMMENT',
			'PERIPHERAL_ID',
			'EQU_TYPE',
			'EQU_NODE',
			'EQU_IDX',
			'EQU_CONNECT',
			'SSTYPE_ID',
			'SUBLOGIC_ID',
			'SUBSYSTEM_ID',
			'SSNODE_ID',
			'SIG_VER',
			'LOCAL_MSGID',
			'REMOTE_MSGID',
			'RMS_VER',
			'RMS_TYPE',
			'RMS_SN_INIT',
			'RMS_SN_MAX',
			'RMS_SN_TABLESIZE'
		]
		global REMOTE_NAME
		for param in map_basic_param:
			if kw[param] == None:
				raise ValueError('input error >> %s in %s\n'%(param, desc))
		equ_Comment				= ";%s" % kw['COMMENT']
		# print('aaa',desc)
		equ_headline			= "["+desc+"]"
		#远端设备名称
		REMOTE_NAME = REMOTE_NAME + desc + ','

		equ_PERIPHERAL_ID		= "PERIPHERAL_ID = %d"		% kw['PERIPHERAL_ID']
		equ_EQU_TYPE			= "EQU_TYPE = %d" 			% kw['EQU_TYPE']
		equ_EQU_NODE			= "EQU_NODE = %d" 			% kw['EQU_NODE']
		equ_EQU_IDX				= "EQU_IDX = %d" 			% kw['EQU_IDX']
		equ_EQU_CONNECT			= "EQU_CONNECT = %s"  		% kw['EQU_CONNECT']
		equ_SSTYPE_ID			= "SSTYPE_ID = %d"    		% kw['SSTYPE_ID']
		equ_SUBLOGIC_ID			= "SUBLOGIC_ID = %d"  		% kw['SUBLOGIC_ID']
		equ_SUBSYSTEM_ID		= "SUBSYSTEM_ID = %d" 		% kw['SUBSYSTEM_ID']
		equ_SSNODE_ID			= "SSNODE_ID = %d"   		% kw['SSNODE_ID']
		equ_SIG_VER				= "SIG_VER = %d" 			% kw['SIG_VER']
		equ_LOCAL_MSGID			= "LOCAL_MSGID = %d" 		% kw['LOCAL_MSGID']
		equ_REMOTE_MSGID		= "REMOTE_MSGID = %d" 		% kw['REMOTE_MSGID']
		equ_RMS_VER				= "RMS_VER = %d" 			% kw['RMS_VER']
		equ_RMS_TYPE			= "RMS_TYPE = %d" 			% kw['RMS_TYPE']
		equ_RMS_SN_INIT			= "RMS_SN_INIT = %d" 		% kw['RMS_SN_INIT']
		equ_RMS_SN_MAX			= "RMS_SN_MAX = %d" 		% kw['RMS_SN_MAX']
		equ_RMS_SN_TABLESIZE	= "RMS_SN_TABLESIZE = %d" 	% kw['RMS_SN_TABLESIZE']

		if kw['EQU_TYPE'] == CVC_APP_TYPE_RSSPI or kw['EQU_TYPE'] == CVC_APP_TYPE_RSSPII :
			equ_EQU_NODE  = "EQU_NODE = 0x%X"	% kw['EQU_NODE']


		self.CVC_EQU_MSG.append([
			equ_Comment,
			equ_headline,
			';MAP',
			equ_PERIPHERAL_ID,
			equ_EQU_TYPE,
			equ_EQU_NODE,
			equ_EQU_IDX,
			equ_EQU_CONNECT,
			';GAPP/MRMS',
			equ_SSTYPE_ID,
			equ_SUBLOGIC_ID,
			equ_SUBSYSTEM_ID,
			equ_SSNODE_ID,
			equ_SIG_VER,
			equ_LOCAL_MSGID,
			equ_REMOTE_MSGID,
			';RMS',
			equ_RMS_VER,
			equ_RMS_TYPE,
			equ_RMS_SN_INIT,
			equ_RMS_SN_MAX,
			equ_RMS_SN_TABLESIZE
		])

		# print(REMOTE_NAME)
		self.__total_link_number = self.__total_link_number + 1
		return

	def AddEquCfg(self, AppType, ConnectRedBlue=True, ConnectCross=False):
		'''
		增加各应用配置，单网、红蓝网、交叉连接形式
		'''
		ConnectParam = 1
		# if ConnectRedBlue == True : ConnectParam = 2
		if ConnectCross == True : ConnectParam = 4  # 4个PID

		# if AppType == CVC_APP_TYPE_SDM : ConnectParam = 2
		
		AppLinkNumber = 0
		if AppType == CVC_APP_TYPE_FUNC		 : AppLinkNumber = ConnectParam * NODE_NUMBER_FUNCTION
		if AppType == CVC_APP_TYPE_FSFB2	 : AppLinkNumber = ConnectParam * NODE_NUMBER_FSFB2
		if AppType == CVC_APP_TYPE_RAW		 : AppLinkNumber = ConnectParam * NODE_NUMBER_RAW
		if AppType == CVC_APP_TYPE_RSSPI	 : AppLinkNumber = ConnectParam * NODE_NUMBER_RSSPI
		if AppType == CVC_APP_TYPE_RSSPII	 : AppLinkNumber = ConnectParam * NODE_NUMBER_RSSPII
		if AppType == CVC_APP_TYPE_SDM		 : AppLinkNumber = ConnectParam * NODE_NUMBER_SDM
		if AppType == CVC_APP_TYPE_REDUNDANCY: AppLinkNumber = ConnectParam * NODE_NUMBER_REDUN

		EquIndex = 0

		MapElement = {
			'Comment'			:0,
            'description'		:0,
            'PERIPHERAL_ID'		:0,
            'EQU_TYPE'			:0,
            'EQU_NODE'			:0,
            'EQU_IDX' 			:0,
            'EQU_CONNECT' 		:0,
            'SSTYPE_ID' 		:0,
            'SUBLOGIC_ID' 		:0,
            'SUBSYSTEM_ID' 		:0,
            'SSNODE_ID' 		:0,
            'SIG_VER' 			:0,
            'LOCAL_MSGID' 		:0,
            'REMOTE_MSGID' 		:0,
            'RMS_VER' 			:0,
            'RMS_TYPE' 			:0,
            'RMS_SN_INIT' 		:0,
            'RMS_SN_MAX' 		:0,
            'RMS_SN_TABLESIZE'	:0
		}

		self.ResetMapDict()
		# self.map_fields.update(appType=AppType)
		global RSSP1_LOCAL_NODE
		global START_PID_FUNC
		global START_PID_FSFB2
		global START_PID_RAW
		global START_PID_RSSPI
		global START_PID_RSSPII
		global START_PID_SDM
		global START_PID_REDUN
		# print('AppLinkNumber=',AppLinkNumber)

		# Remote_name_num = 1
		for x in list(range(AppLinkNumber)):
			while True:
				# print(AppType)

				if AppType == CVC_APP_TYPE_FUNC:
					MapElement['description'] = 'IPS-FUNC-%d' % (x + 1)
					# print('FSFB2:  ',MapElement['description'])
					MapElement['PERIPHERAL_ID'] = START_PID_FUNC
					MapElement['EQU_TYPE'] = CVC_APP_TYPE_FUNC
					MapElement['Comment'] = 'FUNC-%d' % (x + 1)
					MapElement['EQU_NODE'] = (x + 5 + ConnectParam * NODE_NUMBER_FSFB2)
					MapElement['EQU_IDX'] = 0
					MapElement['EQU_CONNECT'] = 'IXL'
					MapElement['SSTYPE_ID'] = 80
					MapElement['SUBLOGIC_ID'] = 2
					MapElement['SUBSYSTEM_ID'] = x + 13
					MapElement['SSNODE_ID'] = MapElement['SSTYPE_ID'] * 256 + MapElement['SUBSYSTEM_ID']
					MapElement['SIG_VER'] = 1
					MapElement['LOCAL_MSGID'] = 1
					MapElement['REMOTE_MSGID'] = 1
					MapElement['RMS_VER'] = 1
					MapElement['RMS_TYPE'] = 1
					MapElement['RMS_SN_INIT'] = 1
					MapElement['RMS_SN_MAX'] = 1000
					MapElement['RMS_SN_TABLESIZE'] = 15
					START_PID_FUNC += 1
					if MapElement['PERIPHERAL_ID'] == 0:
						print('PID is 0')
					break

				if AppType == CVC_APP_TYPE_FSFB2:
					MapElement['description'] = 'IPS-FSFB2-%d' % (x + 1)
					# print('FSFB2:  ',MapElement['description'])
					MapElement['PERIPHERAL_ID'] = START_PID_FSFB2
					MapElement['EQU_TYPE'] = CVC_APP_TYPE_FSFB2
					MapElement['Comment'] = 'FSFB2-%d' % (x + 1)
					MapElement['EQU_NODE'] = (x + 5)
					MapElement['EQU_IDX'] = 0
					MapElement['EQU_CONNECT'] = 'IXL'
					MapElement['SSTYPE_ID'] = 80
					MapElement['SUBLOGIC_ID'] = 2
					MapElement['SUBSYSTEM_ID'] = x + 2
					MapElement['SSNODE_ID'] = MapElement['SSTYPE_ID'] * 256 + MapElement['SUBSYSTEM_ID']
					MapElement['SIG_VER'] = 3
					MapElement['LOCAL_MSGID'] = 1
					MapElement['REMOTE_MSGID'] = 101
					MapElement['RMS_VER'] = 1
					MapElement['RMS_TYPE'] = 1
					MapElement['RMS_SN_INIT'] = 1
					MapElement['RMS_SN_MAX'] = 1000
					MapElement['RMS_SN_TABLESIZE'] = 15
					START_PID_FSFB2 += 1
					if MapElement['PERIPHERAL_ID'] == 0:
						print('PID is 0')
					break

				if AppType == CVC_APP_TYPE_RAW:
					MapElement['description'] = 'IPS-RAW-%d' % (x + 1)
					# print('FSFB2:  ',MapElement['description'])
					MapElement['PERIPHERAL_ID'] = START_PID_RAW
					MapElement['EQU_TYPE'] = CVC_APP_TYPE_RAW
					MapElement['Comment'] = 'RAW-%d' % (x + 1)
					MapElement['EQU_NODE'] = 0
					MapElement['EQU_IDX'] = 0
					MapElement['EQU_CONNECT'] = 'IXL'
					START_PID_RAW += 1
					if MapElement['PERIPHERAL_ID'] == 0:
						print('PID is 0')
					break

				if AppType == CVC_APP_TYPE_RSSPI:
					# print('AppType',AppType)
					if START_PID_RSSPI % 4 == 1 :
						MapElement['description'] = 'IPS-RSSP1-MASTER-%d'	%(RSSP1_LOCAL_NODE-0x7000)
					if START_PID_RSSPI % 4 == 2 :
						MapElement['description'] = 'IPS-RSSP1-SLAVE-%d'	%(RSSP1_LOCAL_NODE-0x7000)
					if START_PID_RSSPI % 4 == 3 :
						MapElement['description'] = 'IPS-RSSP1-MASTER2-%d'	%(RSSP1_LOCAL_NODE-0x7000)
					if START_PID_RSSPI % 4 == 0 :
						MapElement['description'] = 'IPS-RSSP1-SLAVE2-%d'	%(RSSP1_LOCAL_NODE-0x7000)

					# print('RSSP-I:  ',MapElement['description'])
					MapElement['PERIPHERAL_ID']	= START_PID_RSSPI
					MapElement['EQU_TYPE']		= CVC_APP_TYPE_RSSPI
					MapElement['Comment'] 		= 'RSSP1-%d' % (RSSP1_LOCAL_NODE - 0x7000)
					MapElement['EQU_NODE'] 		= RSSP1_LOCAL_NODE
					MapElement['EQU_IDX'] 		= EquIndex
					MapElement['EQU_CONNECT'] 	= 'IXL'
					if START_PID_RSSPI % 4 == 0:
						RSSP1_LOCAL_NODE += 1
						EquIndex += 1
					START_PID_RSSPI += 1
					if MapElement['PERIPHERAL_ID'] == 0:
						print ('PID is 0')
					break

				if AppType == CVC_APP_TYPE_SDM:
					# print('sdm',AppType)
					MapElement['description'] 	= 'DMS-SDM-%d' % (x + 1)
					# print(MapElement['description'])
					MapElement['PERIPHERAL_ID'] = START_PID_SDM
					MapElement['EQU_TYPE'] 		= CVC_APP_TYPE_SDM
					MapElement['Comment'] 		= 'DMS-SDM-%d' % (x + 1)
					MapElement['EQU_NODE'] 		= (x + 1)
					MapElement['EQU_IDX'] 		= 0
					MapElement['EQU_CONNECT'] 	= 'SDM'
					MapElement['SSTYPE_ID'] 	= 90
					MapElement['SUBLOGIC_ID'] 	= 255
					MapElement['SUBSYSTEM_ID'] 	= 1
					MapElement['SSNODE_ID'] 	= 101 + x
					# Remote_name_num += 1
					# MapElement['SSNODE_ID'] +=1
					START_PID_SDM +=1
					if MapElement['PERIPHERAL_ID'] == 0:
						print ('PID is 0')
					break

				if AppType == CVC_APP_TYPE_REDUNDANCY:
					MapElement['description'] = 'IPS-REDUN-%d' % (x + 1)
					# print('FSFB2:  ',MapElement['description'])
					MapElement['PERIPHERAL_ID'] = START_PID_REDUN
					MapElement['EQU_TYPE'] = CVC_APP_TYPE_REDUNDANCY
					MapElement['Comment'] = 'REDUN-%d' % (x + 1)
					MapElement['EQU_NODE'] = 0
					MapElement['EQU_IDX'] = 0
					MapElement['EQU_CONNECT'] = 'IXL'
					MapElement['SSNODE_ID'] = x + 20485

					MapElement['RMS_VER'] = 1
					MapElement['RMS_TYPE'] = 1
					MapElement['RMS_SN_INIT'] = 1
					MapElement['RMS_SN_MAX'] = 1000
					MapElement['RMS_SN_TABLESIZE'] = 15
					START_PID_REDUN += 1
					if MapElement['PERIPHERAL_ID'] == 0:
						print('PID is 0')
					break


			# print(x)
			self.map_fields.update(COMMENT=MapElement['Comment'])
			self.map_fields.update(PERIPHERAL_ID= MapElement['PERIPHERAL_ID'])
			self.map_fields.update(EQU_TYPE=MapElement['EQU_TYPE'])
			self.map_fields.update(EQU_NODE=MapElement['EQU_NODE'])
			self.map_fields.update(EQU_IDX=MapElement['EQU_IDX'])
			self.map_fields.update(EQU_CONNECT=MapElement['EQU_CONNECT'])
			self.map_fields.update(SSTYPE_ID=MapElement['SSTYPE_ID'])
			self.map_fields.update(SUBLOGIC_ID=MapElement['SUBLOGIC_ID'])
			# print('SUBLOGIC_ID = ',MapElement['SUBLOGIC_ID'])
			self.map_fields.update(SUBSYSTEM_ID=MapElement['SUBSYSTEM_ID'])
			self.map_fields.update(SSNODE_ID=MapElement['SSNODE_ID'])
			self.map_fields.update(SIG_VER=MapElement['SIG_VER'])
			# print('SIG_VER = ',MapElement['SIG_VER'])
			self.map_fields.update(LOCAL_MSGID=MapElement['LOCAL_MSGID'])
			self.map_fields.update(REMOTE_MSGID=MapElement['REMOTE_MSGID'])
			self.map_fields.update(RMS_VER=MapElement['RMS_VER'])
			self.map_fields.update(RMS_TYPE=MapElement['RMS_TYPE'])
			self.map_fields.update(RMS_SN_INIT=MapElement['RMS_SN_INIT'])
			self.map_fields.update(RMS_SN_MAX=MapElement['RMS_SN_MAX'])
			self.map_fields.update(RMS_SN_TABLESIZE=MapElement['RMS_SN_TABLESIZE'])
			self.AddBasicMapCfg(desc=MapElement['description'], **self.map_fields)
			# print('desc',MapElement['description'])
		return

	def GetEquAllCfg(self):
		return self.CVC_EQU_MSG

	def CreateEquirmentCfgFile(self):
		'''
		生成配置文件
		'''
		global REMOTE_NAME
		self.AddEquCfg(CVC_APP_TYPE_FUNC)
		self.AddEquCfg(CVC_APP_TYPE_FSFB2)
		self.AddEquCfg(CVC_APP_TYPE_RAW)
		self.AddEquCfg(CVC_APP_TYPE_RSSPI, ConnectCross=True)
		self.AddEquCfg(CVC_APP_TYPE_SDM)
		self.AddEquCfg(CVC_APP_TYPE_REDUNDANCY)

		REMOTE_NAME = REMOTE_NAME[:-1]

		self.AddEquipmentGlobalCfg()
		with io.open('equipment.ini', 'w+', encoding=FileEncodeType) as file:
			for field in self.CVC_EQU_MSG:
				for cell in field:
					file.write(cell + '\n')
				file.write('\n')
		return


#==========================================================
#CreateProtocolsFile
#==========================================================
class ProtocolsConfig(object):
	'''
	@ Protocol.ini配置生成
	'''

	CVC200_ASW_CFG = []

	# Red_Remote_Ip_Cfg = []
	# Blue_Remote_Ip_Cfg = []

	def __init__(self, EquCfg):
		self.__local_line_number = 0
		self.__dest_SerialLink_Num = 0
		self.__dest_CanLink_Num = 0
		self.__dest_EtherLink_Num = 0
		self.__rssp_cross_count = 0
		self.__sdm_link_count = 0
		self.__map_all_cfg = EquCfg
		self.__local_line_cfg = []
		self.__local_line_segment = {}

		for Net in LOCAL_NET_IP.values():
			L_IP, L_MASK = Net.split(':')
			NetSeg = IP(L_IP).make_net(L_MASK).strNormal(0)
			#print 'NetSeg',IP(L_IP),IP(L_IP).make_net(L_MASK),IP(L_IP).make_net(L_MASK).strNormal(0)
			self.__local_line_segment[NetSeg] = REMOTE_NET_IP_INIT
		# print ('__local_line_segment',(self.__local_line_segment))

	def AddProGlobalCfg(self):
		'''
		@ 增加全局字段
		'''
		self.CVC200_ASW_CFG.append([
			';fsfb2消息的可用周期(7),编码类型SINGLE',
			'[FSFB2]',
			'FSFB2_AVAILABLE = 7',
			'FSFB2_CODE_TYPE = 0',
		])
		self.CVC200_ASW_CFG.append([
			'[MSS]',
			'RED_NET_IP = 0.0.0.0',
			'BLUE_NET_IP = 0.0.0.0',
			'LOCAL_NO = 0',
		])
		return


	def AddAswLocalEtherLineCfg(self):
		'''
		@ 增加本地网络字段
		'''

		self.CVC200_ASW_CFG.append([

			';本地设备协议参数信息',
			'[LOCAL_EQUIPMENT]',
			'NUM = %d' % len(LOCAL_NET_IP)
		])

		for Board_Net_NO in LOCAL_NET_IP.keys():

			#Local_Network_Port = Board_Port.split('_')[-1]
			#print 'Local_Network_Port',Local_Network_Port
			# print ("AddAswLocalEtherLineCfg Board_Net_NO", Board_Net_NO)
			Local_IP = LOCAL_NET_IP[Board_Net_NO].split(':')[0]
			# print('Local_IP = %s' %Local_IP )
			Local_Subnet_Mask = LOCAL_NET_IP[Board_Net_NO].split(':')[1]

			#if int(Local_Network_Port) > 3: raise ValueError('Local NetWork Port Error >> %s' % Local_Network_Port)

			self.CVC200_ASW_CFG.append([

				'[LOCAL_%d]'	% self.__local_line_number,
				'NET_IP = %s'	% Local_IP,
				'MASK = %s'		% Local_Subnet_Mask,
				'GATEWAY = 172.17.9.126',
				'USED_NETPORT = %s' % Board_Net_NO
			])

			# 存放本地IP用于远端Link的生成
			self.__local_line_cfg.append(Local_IP)
			self.__local_line_number += 1
		#print 'self.CVC200_ASW_CFG',self.CVC200_ASW_CFG
		return


	def GetAswDestEtherLinkNum(self):
		'''
		@ 远端设备数量，设备数量减去两个本地设备
		'''
		return int(self.__map_all_cfg[4][2].split('=')[-1]) - 2
	# def GetDestEtherName(self, target, MapLinkCfg, isNumber=False, isString=False):
	# 	'''
	# 	@ 从 MAP 中获取远端LINK需要的配置信息
	# 	'''
    #
	# 	result = None
    #
	# 	if isNumber == isString: raise ValueError('data type conflict >> %s' % target)
    #
	# 	for field in MapLinkCfg:
	# 		if target in field:
	# 			if isNumber == True: result = int(field.split('=')[-1])
	# 			if isString == True: result = field.split('=')[-1]
    #
	# 	if result == None: raise ValueError('%s not found in >> %s' % (target, MapLinkCfg))
	# 	return result
	def GetDestEtherMapCfg(self, target, MapLinkCfg, isNumber=False, isString=False):
		'''
		@ 从 MAP 中获取远端LINK需要的配置信息
		'''

		result = None

		if isNumber == isString:
			raise ValueError('data type conflict >> %s' % target)

		for field in MapLinkCfg:
			if target in field:
				if isNumber == True:
					result = int(field.split('=')[-1])
				if isString == True:
					result = field.split('=')[-1]

		if result == None:
			raise ValueError('%s not found in >> %s' % (target, MapLinkCfg))
		return result

	def GetDestEtherRemoteIpPort(self, l_ip, l_mask, app_Type):
		'''
		@ 获取远端地址
		'''
		UsedNetSeg = IP(l_ip).make_net(l_mask).strNormal(0)
		# print ("wwwwww",IP(l_ip),IP(l_ip).make_net(l_mask),IP(l_ip).make_net(l_mask).strNormal(0))
		# print ('GetDestEtherRemoteIpPort UsedNetSeg',UsedNetSeg)
		CurUsedIdx = self.__local_line_segment[UsedNetSeg]
		# print ('GetDestEtherRemoteIpPort CurUsedIdx',CurUsedIdx)
		# print('UsedNetSeg',UsedNetSeg)
		remote_ip = UsedNetSeg.replace('.0.', '.%d.' % app_Type)
		# print('remote_ip', remote_ip)
		remote_ip = remote_ip.replace('.0', '.%d' % CurUsedIdx)
		# print ('GetDestEtherRemoteIpPort remote_ip',remote_ip)
		self.__local_line_segment[UsedNetSeg] += 1

		remote_port = self.__local_line_segment[UsedNetSeg] - REMOTE_NET_IP_INIT + REMOTE_NET_PORT_INIT

		return remote_ip, remote_port

	# def GetLocalUsedLineByLocalIp(self, l_ip):
	# 	'''
	# 	@ 通过本地IP获取used_local_line_idx
	# 	'''
	# 	for local_line_idx in list(range(len(self.__local_line_cfg))):
	# 		if self.__local_line_cfg[local_line_idx] == l_ip:
	# 			return local_line_idx
	# 	raise ValueError('local line index not found > %s' % l_ip)

	# return

	def GetDestEtherRemoteCfg(self, app_type, PID):
		'''
		@ 依据LINK类型获取远端IP, 使用的 local_line_idx
		'''
		# print ("GetDestEtherRemoteCfg app_type:",app_type)
		if isinstance(app_type, int) == False:
			raise ValueError('data type conflict > %d, %d' % (isinstance(app_type, int), isinstance(Board_ID, int)))

		while True:
			isCrossConnectUsed = False
			if app_type == CVC_APP_TYPE_FUNC:
				if PID % 2 == 1:
					UsedLocalNetNo_R = LOCAL_USED_BY_FUNC[0]
					UsedLocalNetNo_B = LOCAL_USED_BY_FUNC[1]
				else:
					UsedLocalNetNo_R = LOCAL_USED_BY_FUNC[2]
					UsedLocalNetNo_B = LOCAL_USED_BY_FUNC[3]
				break

			if app_type == CVC_APP_TYPE_FSFB2:
				UsedLocalNetNo_R = LOCAL_USED_BY_FSFB2[0]
				UsedLocalNetNo_B = LOCAL_USED_BY_FSFB2[1]
				break

			if app_type == CVC_APP_TYPE_RAW:
				UsedLocalNetNo_R = LOCAL_USED_BY_RAW[0]
				UsedLocalNetNo_B = LOCAL_USED_BY_RAW[1]
				break

			if app_type == CVC_APP_TYPE_SDM:
				UsedLocalNetNo_R = LOCAL_USED_BY_SDM_A[0], LOCAL_USED_BY_SDM_A[1]
				UsedLocalNetNo_B = LOCAL_USED_BY_SDM_B[0], LOCAL_USED_BY_SDM_B[1]
				break

			if app_type == CVC_APP_TYPE_REDUNDANCY:
				UsedLocalNetNo_R = LOCAL_USED_BY_REDUN[0]
				UsedLocalNetNo_B = LOCAL_USED_BY_REDUN[1]
				break

			if app_type == CVC_APP_TYPE_RSSPI:
				if PID % 4 == 1:
					#红蓝网
					UsedLocalNetNo_R = LOCAL_USED_BY_RSSP1_A[0]
					UsedLocalNetNo_B = LOCAL_USED_BY_RSSP1_A[1]
					# print ('GetDestEtherRemoteCfg UsedLocalNetNo:',UsedLocalNetNo_B)
				elif PID % 4 == 2:
					UsedLocalNetNo_R = LOCAL_USED_BY_RSSP1_B[0]
					UsedLocalNetNo_B = LOCAL_USED_BY_RSSP1_B[1]
				elif PID % 4 == 3:
					#红蓝网
					UsedLocalNetNo_R = LOCAL_USED_BY_RSSP1_A[2]
					UsedLocalNetNo_B = LOCAL_USED_BY_RSSP1_A[3]
					#print 'GetDestEtherRemoteCfg UsedLocalNetNo:',UsedLocalNetNo
				else:
					UsedLocalNetNo_R = LOCAL_USED_BY_RSSP1_B[2]
					UsedLocalNetNo_B = LOCAL_USED_BY_RSSP1_B[3]
				break

		if app_type == CVC_APP_TYPE_SDM:
			local_ip_R1, local_mask_R1 = LOCAL_NET_IP[UsedLocalNetNo_R[0]].split(':')
			local_ip_R2, local_mask_R2 = LOCAL_NET_IP[UsedLocalNetNo_R[1]].split(':')
			local_ip_B1, local_mask_B1 = LOCAL_NET_IP[UsedLocalNetNo_B[0]].split(':')
			local_ip_B2, local_mask_B2 = LOCAL_NET_IP[UsedLocalNetNo_B[1]].split(':')
			remote_ip_R1, remote_port_R1 = self.GetDestEtherRemoteIpPort(local_ip_R1, local_mask_R1, app_type)
			remote_ip_R2, remote_port_R2 = self.GetDestEtherRemoteIpPort(local_ip_R2, local_mask_R2, app_type)
			# print(remote_ip_R, remote_port_R)
			remote_ip_B1, remote_port_B1 = self.GetDestEtherRemoteIpPort(local_ip_B1, local_mask_B1, app_type)
			remote_ip_B2, remote_port_B2 = self.GetDestEtherRemoteIpPort(local_ip_B2, local_mask_B2, app_type)
			# print('wwwwww',remote_ip_R1, remote_port_R1, UsedLocalNetNo_R[0], remote_ip_R2, remote_port_R2, UsedLocalNetNo_R[1], \
			# 	   remote_ip_B1, remote_port_B1, UsedLocalNetNo_B[0], remote_ip_B2, remote_port_B2, UsedLocalNetNo_B[1])
			return remote_ip_R1, remote_port_R1, UsedLocalNetNo_R[0], remote_ip_R2, remote_port_R2, UsedLocalNetNo_R[1], \
				   remote_ip_B1, remote_port_B1, UsedLocalNetNo_B[0], remote_ip_B2, remote_port_B2, UsedLocalNetNo_B[1]
		else:
			local_ip_R, local_mask_R = LOCAL_NET_IP[UsedLocalNetNo_R].split(':')
			# print(local_ip_R, local_mask_R)
			local_ip_B, local_mask_B = LOCAL_NET_IP[UsedLocalNetNo_B].split(':')
			# local_port = LOCAL_NET_PORT_INIT + app_type

			remote_ip_R, remote_port_R = self.GetDestEtherRemoteIpPort(local_ip_R, local_mask_R, app_type)
			# print(remote_ip_R, remote_port_R)
			remote_ip_B, remote_port_B = self.GetDestEtherRemoteIpPort(local_ip_B, local_mask_B, app_type)
			# print(UsedLocalNetNo_R,UsedLocalNetNo_B)
			# print('qqqqqqq',remote_ip_R, remote_port_R, UsedLocalNetNo_R, remote_ip_B, remote_port_B, UsedLocalNetNo_B)
			return remote_ip_R, remote_port_R, UsedLocalNetNo_R, remote_ip_B, remote_port_B, UsedLocalNetNo_B


	def GetLocalNetNumber(self,NetNO):
		Count = 0
		for field in LOCAL_NET_IP:
			if NetNO == field:
				break
			Count+=1
		return Count


	def AddAswDestEthetLinkCfg(self):
		'''
		@ 增加外部网络链接数据
		'''
		self.CVC200_ASW_CFG.append([
			';远端设备协议参数信息',
			'[REMOTE_EQUIPMENT]',
			'NUM = %d' % self.GetAswDestEtherLinkNum(),
		])
		DestLinkElement = {
			'NAME'				:	0,
			'NET_NUM'			:	0,
			'UDPOrTCP'			:	0,
			'ClientOrServer'	:	0,
			'NET_IP_0'			:	0,
			'MASK_0'			:	0,
			'LOCAL_PORT_0'		:	0,
			'REMOTE_PORT_0'		: 	0,
			'USED_LOCAL_NO_0'	:	0,
			'NET_IP_1'			:	0,
			'MASK_1'			:	0,
			'LOCAL_PORT_1'		:	0,
			'REMOTE_PORT_1'		:	0,
			'USED_LOCAL_NO_1'	:	0,

		}
		DestLinkElement_SDM = {
			'NET_IP_2'	 		:	0,
			'MASK_2'		 	:	0,
			'LOCAL_PORT_2'	 	:	0,
			'REMOTE_PORT_2'	 	:	0,
			'USED_LOCAL_NO_2'	:	0,
			'NET_IP_3'	 		:	0,
			'MASK_3'		 	:	0,
			'LOCAL_PORT_3'	 	:	0,
			'REMOTE_PORT_3'	 	:	0,
			'USED_LOCAL_NO_3'	:	0,
		}

		for Link_info in self.__map_all_cfg[7:]:
			# print ("Link_info",Link_info)

			if 'EQU_TYPE = 12' in Link_info:
				# 过滤掉STBY的配置
				continue
			DestLinkElement['NAME'] = Link_info[1].strip('[]')
			if 'EQU_TYPE = 13' in Link_info:
			# if(Link_info[1].strip('[]') == 'IPS-SDM'):
				DestLinkElement['NET_NUM'] = 4
			else:
				DestLinkElement['NET_NUM'] = 2
			if 'EQU_TYPE = 5' in Link_info:
				DestLinkElement['UDPOrTCP'] = 'TCP'
			else:
				DestLinkElement['UDPOrTCP'] = 'UDP'

			DestLinkElement['ClientOrServer'] = 'CLIENT'
			# DestNetCfg = self.GetDestEtherRemoteCfg( self.GetDestEtherMapCfg('EQU_TYPE', Link_info, isNumber=True),self.GetDestEtherMapCfg('PERIPHERAL_ID', Link_info, isNumber=True))
			# print(DestNetCfg)
			#LOCAL_NET_IP
			if 'EQU_TYPE = 13' in Link_info:
				DestNetCfg = self.GetDestEtherRemoteCfg(self.GetDestEtherMapCfg('EQU_TYPE', Link_info, isNumber=True),\
				 										self.GetDestEtherMapCfg('PERIPHERAL_ID', Link_info,	isNumber=True))
				# print('qqqq',DestNetCfg)
				[remote_ip_R1, Remote_Port_R1, UsedLocalNetNo_R1, remote_ip_R2, Remote_Port_R2, UsedLocalNetNo_R2,\
				 remote_ip_B1, Remote_Port_B1, UsedLocalNetNo_B1, remote_ip_B2, Remote_Port_B2, UsedLocalNetNo_B2] = DestNetCfg
				# print('aaaaa',remote_ip_R1)
				# print('sssssss',remote_ip_R1, Remote_Port_R1, UsedLocalNetNo_R1, remote_ip_R2, Remote_Port_R2, UsedLocalNetNo_R1,\
				#  remote_ip_B1, Remote_Port_B1, UsedLocalNetNo_B1, remote_ip_B2, Remote_Port_B2, UsedLocalNetNo_B1)

				DestLinkElement['NET_IP_0'] 			= remote_ip_R1
				DestLinkElement['MASK_0'] 				= LOCAL_NET_IP[UsedLocalNetNo_R1].split(':')[1]
				DestLinkElement['LOCAL_PORT_0'] 		= Remote_Port_R1
				DestLinkElement['REMOTE_PORT_0'] 		= Remote_Port_R1
				DestLinkElement['USED_LOCAL_NO_0'] 		= self.GetLocalNetNumber(UsedLocalNetNo_R1)
				DestLinkElement['NET_IP_1'] 			= remote_ip_B1
				DestLinkElement['MASK_1'] 				= LOCAL_NET_IP[UsedLocalNetNo_B1].split(':')[1]
				DestLinkElement['LOCAL_PORT_1'] 		= Remote_Port_B1
				DestLinkElement['REMOTE_PORT_1'] 		= Remote_Port_B1
				DestLinkElement['USED_LOCAL_NO_1'] 		= self.GetLocalNetNumber(UsedLocalNetNo_B1)
				DestLinkElement_SDM['NET_IP_2'] 		= remote_ip_R2
				DestLinkElement_SDM['MASK_2'] 			= LOCAL_NET_IP[UsedLocalNetNo_R2].split(':')[1]
				DestLinkElement_SDM['LOCAL_PORT_2'] 	= Remote_Port_R2
				DestLinkElement_SDM['REMOTE_PORT_2'] 	= Remote_Port_R2
				DestLinkElement_SDM['USED_LOCAL_NO_2'] 	= self.GetLocalNetNumber(UsedLocalNetNo_R2)
				DestLinkElement_SDM['NET_IP_3'] 		= remote_ip_B2
				DestLinkElement_SDM['MASK_3'] 			= LOCAL_NET_IP[UsedLocalNetNo_B2].split(':')[1]
				DestLinkElement_SDM['LOCAL_PORT_3'] 	= Remote_Port_B2
				DestLinkElement_SDM['REMOTE_PORT_3'] 	= Remote_Port_B2
				DestLinkElement_SDM['USED_LOCAL_NO_3'] 	= self.GetLocalNetNumber(UsedLocalNetNo_B2)

			else:
				DestNetCfg = self.GetDestEtherRemoteCfg(self.GetDestEtherMapCfg('EQU_TYPE', Link_info, isNumber=True), \
														self.GetDestEtherMapCfg('PERIPHERAL_ID', Link_info,	isNumber=True))
				# print('aaaaaa', DestNetCfg)
				[remote_ip_R, Remote_Port_R, UsedLocalNetNo_R, remote_ip_B, Remote_Port_B, UsedLocalNetNo_B] = DestNetCfg
				DestLinkElement[ 'NET_IP_0']			= remote_ip_R
				DestLinkElement['MASK_0'] 				= LOCAL_NET_IP[UsedLocalNetNo_R].split(':')[1]
				DestLinkElement['LOCAL_PORT_0'] 		= Remote_Port_R
				DestLinkElement['REMOTE_PORT_0'] 		= Remote_Port_R
				DestLinkElement['USED_LOCAL_NO_0'] 		= self.GetLocalNetNumber(UsedLocalNetNo_R)
				DestLinkElement['NET_IP_1'] 			= remote_ip_B
				DestLinkElement['MASK_1'] 				= LOCAL_NET_IP[UsedLocalNetNo_B].split(':')[1]
				DestLinkElement['LOCAL_PORT_1'] 		= Remote_Port_B
				DestLinkElement['REMOTE_PORT_1'] 		= Remote_Port_B
				DestLinkElement['USED_LOCAL_NO_1'] 		= self.GetLocalNetNumber(UsedLocalNetNo_B)



			Ether_description			= ';'
			Ether_REMOTE 				= '[REMOTE_%d]' 			% self.__dest_EtherLink_Num
			Ether_NAME 					= 'NAME = %s'				% DestLinkElement['NAME']
			Ether_NET_NUM				= 'NET_NUM = %d'			% DestLinkElement['NET_NUM']
			Ether_UDPOrTCP 				= 'UDPOrTCP = %s'			% DestLinkElement['UDPOrTCP']
			Ether_ClientOrServer		= 'ClientOrServer = %s'		% DestLinkElement['ClientOrServer']
			Ether_space 				= ';'
			Ether_NET_IP_0				= 'NET_IP_0 = %s'			% DestLinkElement[ 'NET_IP_0']
			Ether_MASK_0				= 'MASK_0 = %s'				% DestLinkElement[ 'MASK_0']
			Ether_LOCAL_PORT_0			= 'LOCAL_PORT_0 = %d' 		% DestLinkElement[ 'LOCAL_PORT_0']
			Ether_REMOTE_PORT_0			= 'REMOTE_PORT_0 = %d'		% DestLinkElement[ 'REMOTE_PORT_0']
			Ether_USED_LOCAL_NO_0		= 'USED_LOCAL_NO_0 = %d'	% DestLinkElement[ 'USED_LOCAL_NO_0']
			Ether_NET_IP_1				= 'NET_IP_1 = %s' 			% DestLinkElement[ 'NET_IP_1']
			Ether_MASK_1				= 'MASK_1 = %s'				% DestLinkElement[ 'MASK_1']
			Ether_LOCAL_PORT_1			= 'LOCAL_PORT_1 = %d'		% DestLinkElement[ 'LOCAL_PORT_1']
			Ether_REMOTE_PORT_1			= 'REMOTE_PORT_1 = %d'		% DestLinkElement[ 'REMOTE_PORT_1']
			Ether_USED_LOCAL_NO_1		= 'USED_LOCAL_NO_1 = %d'	% DestLinkElement[ 'USED_LOCAL_NO_1']
			Ether_NET_IP_2 				= 'NET_IP_2 = %s' 			% DestLinkElement_SDM['NET_IP_2']
			Ether_MASK_2 				= 'MASK_2 = %s'				% DestLinkElement_SDM['MASK_2']
			Ether_LOCAL_PORT_2 			= 'LOCAL_PORT_2 = %d' 		% DestLinkElement_SDM['LOCAL_PORT_2']
			Ether_REMOTE_PORT_2 		= 'REMOTE_PORT_2 = %d' 		% DestLinkElement_SDM['REMOTE_PORT_2']
			Ether_USED_LOCAL_NO_2	   	= 'USED_LOCAL_NO_2 = %d' 	% DestLinkElement_SDM['USED_LOCAL_NO_2']
			Ether_NET_IP_3 			 	= 'NET_IP_3 = %s'			% DestLinkElement_SDM['NET_IP_3']
			Ether_MASK_3 			  	= 'MASK_3 = %s' 			% DestLinkElement_SDM['MASK_3']
			Ether_LOCAL_PORT_3 		  	= 'LOCAL_PORT_3 = %d'		% DestLinkElement_SDM['LOCAL_PORT_3']
			Ether_REMOTE_PORT_3 		= 'REMOTE_PORT_3 = %d'	 	% DestLinkElement_SDM['REMOTE_PORT_3']
			Ether_USED_LOCAL_NO_3 	   	= 'USED_LOCAL_NO_3 = %d'	% DestLinkElement_SDM['USED_LOCAL_NO_3']




			self.CVC200_ASW_CFG.append([
				Ether_description,
				Ether_REMOTE,
				Ether_NAME,
				Ether_NET_NUM,
				Ether_UDPOrTCP,
				Ether_ClientOrServer,
				Ether_space,
				Ether_NET_IP_0,
				Ether_MASK_0,
				Ether_LOCAL_PORT_0,
				Ether_REMOTE_PORT_0,
				Ether_USED_LOCAL_NO_0,
				Ether_space,
				Ether_NET_IP_1,
				Ether_MASK_1,
				Ether_LOCAL_PORT_1,
				Ether_REMOTE_PORT_1,
				Ether_USED_LOCAL_NO_1,
			])
			if 'EQU_TYPE = 13' in Link_info:
				self.CVC200_ASW_CFG.append([
					Ether_space,
					Ether_NET_IP_2,
					Ether_MASK_2,
					Ether_LOCAL_PORT_2,
					Ether_REMOTE_PORT_2,
					Ether_USED_LOCAL_NO_2,
					Ether_space,
					Ether_NET_IP_3,
					Ether_MASK_3,
					Ether_LOCAL_PORT_3,
					Ether_REMOTE_PORT_3,
					Ether_USED_LOCAL_NO_3
				])

			self.__dest_EtherLink_Num += 1
		return

	# def GetRemoteIPCfg(self):
	# 	return self.Remote_Ip_Cfg

	def CreateProCfgFile(self):
		'''
		@ 创建并生成CVC200_Config_ASW.ini
		'''

		self.AddProGlobalCfg()
		self.AddAswLocalEtherLineCfg()
		self.AddAswDestEthetLinkCfg()
		with io.open('protocols.ini', 'w+', encoding=FileEncodeType) as file:
			for fields in self.CVC200_ASW_CFG:
				for cell in fields:
					#print "cell",cell
					file.write(cell + '\n')
				file.write('\n')

		#with open('setallip.bat', 'w+', encoding=FileEncodeType) as _f:
			#for _ip in self.Red_Remote_Ip_Cfg:
				#_f.write("netsh interface ip add address name=\"Red\" addr=%s mask=255.255.255.0\n"% ( _ip))

			#for _ip in self.Blue_Remote_Ip_Cfg:
				#_f.write("netsh interface ip add address name=\"Blue\" addr=%s mask=255.255.255.0\n"% ( _ip))

		return
		

 



if __name__ == '__main__':
	equ =Equipment()
	equ.CreateEquirmentCfgFile()

	pro = ProtocolsConfig(equ.GetEquAllCfg())
	pro.CreateProCfgFile()
	 


	