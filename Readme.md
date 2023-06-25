# 티스토리 자동댓글/자동공감 매크로
티스토리 블로그. 자동으로 구독을 눌러서 구독자를 늘려줍니다. 늘린 구독 블로그를 바탕으로 피드 리스트를 생성하거나 티스토리 스토리에 있는 블로그들을 대상으로 피드 리스트를 생성할 수 있습니다.   
생성된 피드 리스트로 자동으로 댓글을 쓰고, 공감을 누를 수 있습니다.   
자세한 내용은 [limetimeline tistory](https://limetimeline.tistory.com/537)   

Release Version 1.0   

Recent Update: 2023-06-26   

# UpdateNotes
2023-06-26 - release version 1.0.0   
- 블로그 주소가 'https://000.tistory.com/나는-오늘-좋았다' 형식이면 건너뜀 (https://000.tistory.com/420 형식만 가능)
- 피드 리스트, 스토리 피드 리스트를 메모장으로 저장하고 불러오기 기능
- 이미 구독된 블로그 건너뛰기
- 댓글쓰기 및 공감 누르기 기능

# Requirements
- Python 3.7
- Selenium

# Useage
```python
python autoComment.py
```
- 반드시 로그인하고 사용하세요!
- (구독자가 없을 때) 3. 구독늘리기 → 1. 구독자 피드 리스트 생성 → 2. 댓글 쓰기 및 공감 누르기
- (구독자가 있을 때) 1. 구독자 피드 리스트 생성 → 2. 댓글 쓰기 및 공감 누르기
- (구독자가 있든 없든) 4. 스토리 피드 리스트 생성 → 2. 댓글 쓰기 및 공감 누르기
- 피드 리스트 불러오기 5. PostList 불러오기(postList.txt)
