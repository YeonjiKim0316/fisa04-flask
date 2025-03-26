# Blueprint 기능을 사용해서 collection/no1/
# Blueprint 기능을 사용해서 collection/no2/
@app.route('/collection')
    def hello2():
        return f'{__name__} 첫번째'
    
    @app.route('/collection/test')
    def hello3():
        return f'{__name__} 두번째'
    