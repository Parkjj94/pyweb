from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from board.models import Question, Answer, Comment
from board.forms import QuestionForm, AnswerForm, CommentForm

@login_required(login_url='common:login')
def comment_create_answer(request, answer_id):
    # 답변 댓글 등록
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.method == "POST":
        form = CommentForm(request.POST) #입력된 댓글 내용
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user   # 세션 권한
            comment.create_date = timezone.now()
            comment.answer = answer     # 참조 외래키
            comment.save()              # 실제 저장
            return redirect('board:detail', question_id=comment.answer.question.id)
    else:   # GET은 빈 폼을 가져옴
        form = CommentForm()
    context = {'form':form}
    return render(request, 'board/comment_form.html', context)

@login_required(login_url='common:login')
def comment_delete_answer(request, comment_id):
    # 답변 댓글 삭제
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글삭제권한이 없습니다')
        return redirect('board:detail', question_id=comment.answer.question.id)
    else:
        comment.delete()
    return redirect('board:detail', question_id=comment.answer.question.id)

@login_required(login_url='common:login')
def comment_modify_answer(request, comment_id):
    # 답변 댓글 수정
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글수정권한이 없습니다')
        return redirect('board:detail', question_id=comment.answer.question.id)
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment) #변경된 내용 입력
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user  # 세션 권한
            comment.modify_date = timezone.now()
            comment.save()  # 실제 저장
            return redirect('board:detail', question_id=comment.answer.question.id)
    else:
        form = CommentForm(instance=comment)    #채워진 폼
    context = {'form':form}
    return render(request, 'board/comment_form.html', context)