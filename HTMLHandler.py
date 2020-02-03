def allClosed( dictionary ):
    result = sum( [ int( dictionary[key] ) for key in dictionary  ] )
    
    if result == 0:
        return True
    else:
        return False

def isValidTag( char ):
    return char == '<'

def isSlashTag( char ):
    return (char == '\'' or char == '/')

def getTagName( index, source ):
    tagName, lenSource, up = '', len(source), 1
    index += 1
    
    if isSlashTag( source[index] ):
        up = -1
        index += 1
    
    while True:
        char = source[index]
        
        if char.isalpha():
            tagName += char
        else:
            break
        
        index += 1
        
    return (tagName, up)

def isUniqueTag( tag ):
    uniqueTags = ['img', 'br', 'wbr']
    
    return tag in uniqueTags

def updateTagNameValue(dictionary, key, up):
    #disposableTags = ['wbr']
    if isUniqueTag( key ):
        up = 0
    
    if key in dictionary:
        dictionary[key] += up
    else:
        dictionary[key] = up
    
    if dictionary[key] < 0:
        dictionary[key] = 0

def getScopeTag(index, source):
    controler, scope, start, end = {}, '', index, index
    #print('to>', source[start:start+20])
    while True:
        try:
            char = source[index]
            
            if isValidTag( char ):
                tagName, up = getTagName(index, source)
                updateTagNameValue( controler, tagName, up )
                #print(source[index:index+100], controler)
            
            end += 1
            
            if allClosed( controler ):
                end += source[index:].find('>')
                break
            
            index += 1
        except:
            #print('gerou excecao')
            break
        
    scope = source[start:end]
    return scope

def extractLink(tag):
    attr, link = 'href="', ''
    
    if attr in tag:
        index = tag.find( attr ) + len( attr )
        
        while tag[index] != '"':
            link += tag[index]
            index += 1
        
        return link
    else:
        return None

def stripTags(value):
    while True:
        try:
            lt = value.index('<')
            mt = lt + value[lt:].index('>')
            value = value[0:lt] + value[mt+1:]
        except:
            break
    return value