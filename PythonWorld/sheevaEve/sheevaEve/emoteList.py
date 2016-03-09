def getValueForKey(key):
    emoteList=dict()
    emoteList["e6020058"]=0X1
    emoteList["e7020058"]=0X3
    emoteList["810d0058"]=0X33
    emoteList["7c0d0058"]=0X30
    emoteList["7b0d0058"]=0X2F
    emoteList["7d0d0058"]=0X31
    emoteList["0e00003a"]=0X10
    emoteList["0c00003a"]=0X16
    emoteList["9b010058"]=0X2
    emoteList["970d0058"]=0X5C
    emoteList["9c0d0058"]=0X65
    emoteList["bf0200b4"]=0X76
    emoteList["cc0200b4"]=0X77
    emoteList["9d0d0058"]=0X68
    emoteList["590d0058"]=0X8
    emoteList["570d0058"]=0X7
    emoteList["1100003a"]=0X6
    emoteList["940d0058"]=0X58
    emoteList["5a0d0058"]=0X13
    emoteList["580d0058"]=0X12
    emoteList["1200003a"]=0X66
    emoteList["150e0058"]=0X72
    emoteList["ef0c0058"]=0X17
    emoteList["170e0058"]=0X1B
    emoteList["f00c0058"]=0X19
    emoteList["f30c0058"]=0X1F
    emoteList["1f0e0058"]=0X79
    emoteList["190e0058"]=0X7D
    emoteList["110e0058"]=0X7E
    emoteList["f60c0058"]=0X1D
    emoteList["0400003a"]=0XA
    emoteList["1300003a"]=0XC
    emoteList["1400003a"]=0XD
    emoteList["d1020058"]=0XB
    emoteList["f50c0058"]=0XE
    emoteList["fa0c0058"]=0XF
    emoteList["0d00003a"]=0X4
    emoteList["fb0c0058"]=0X21
    emoteList["920d0058"]=0X54
    emoteList["270d0058"]=0X2B
    emoteList["1f0d0058"]=0X2A
    emoteList["0d0e0058"]=0X7F
    emoteList["960d0058"]=0X5A
    emoteList["130d0058"]=0X29
    emoteList["e9020058"]=0X14
    emoteList["7a0d0058"]=0X2E
    emoteList["880200b4"]=0X73
    emoteList["7e0d0058"]=0X34
    emoteList["a40d0058"]=0X56
    emoteList["770d0058"]=0X5B
    emoteList["a50d0058"]=0X6F
    emoteList["250e0058"]=0X78
    emoteList["a9150058"]=0X35
    emoteList["1000003a"]=0X5
    emoteList["0f00003a"]=0X15
    emoteList["f40c0058"]=0X22
    emoteList["650d0058"]=0X2D
    emoteList["b70d0058"]=0X71
    emoteList["990d0058"]=0X60
    emoteList["fd0d0058"]=0XCA
    emoteList["f50d0058"]=0XD6
    emoteList["e4020058"]=0XC1
    emoteList["fb0d0058"]=0XD3
    emoteList["050e0058"]=0XD9
    emoteList["ff0d0058"]=0XD0
    emoteList["010e0058"]=0XDF
    emoteList["ff0d0058"]=0XD0
    emoteList["030e0058"]=0XDC
    emoteList["ca0d0058"]=0XCD
    emoteList["05160058"]=0XE8
    
    try:
	result = emoteList[key]
	return result
    except:
	return -1 # that's key error exception, but anyway