class Pagination:
    def __init__(self, collection, items_per_page=10, pages_per_list=5):
        self.collection = collection  # MongoDB 컬렉션
        self.items_per_page = items_per_page  # 한 페이지에 표시할 아이템 수
        self.pages_per_list = pages_per_list  # 한 페이지 리스트에 표시할 페이지 수
        self.current_page = 1  # 현재 페이지 번호
        self.total_items = collection.count_documents({})  # 전체 아이템 수
        self.total_pages = (self.total_items + items_per_page - 1) // items_per_page  # 전체 페이지 수

    def get_page(self, page_number):
        # 주어진 페이지 번호의 아이템을 가져옴
        self.current_page = page_number
        skips = self.items_per_page * (page_number - 1)
        items = self.collection.find().skip(skips).limit(self.items_per_page)
        return list(items)

    def next_page(self):
        # 다음 페이지의 아이템을 가져옴
        return self.get_page(self.current_page + 1)

    def prev_page(self):
        # 이전 페이지의 아이템을 가져옴
        return self.get_page(self.current_page - 1)

    def first_page(self):
        # 첫 페이지의 아이템을 가져옴
        return self.get_page(1)

    def last_page(self):
        # 마지막 페이지의 아이템을 가져옴
        return self.get_page(self.total_pages)

    def prev_page_list(self):
        # 이전 페이지 리스트의 아이템을 가져옴
        start_page = ((self.current_page - 1) // self.pages_per_list) * self.pages_per_list
        return [self.get_page(i) for i in range(start_page, start_page + self.pages_per_list)]

    def next_page_list(self):
        # 다음 페이지 리스트의 아이템을 가져옴
        start_page = ((self.current_page + self.pages_per_list - 1) // self.pages_per_list) * self.pages_per_list + 1
        end_page = min(start_page + self.pages_per_list, self.total_pages + 1)
        return [self.get_page(i) for i in range(start_page, end_page)]
