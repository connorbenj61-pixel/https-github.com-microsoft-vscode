def sort_objects(objs):
	return sorted(objs, key=lambda x: x['key'])

if __name__ == '__main__':
objs = [{'key':3,'name':'c'},{'key':1,'name':'a'},{'key':2,'name':'b'}]
print(sort_objects(objs))
