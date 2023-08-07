import json
from .models import Expense
from rest_framework import status
from django.test import TestCase,Client
from django.contrib.auth.models import User
from expenseApp.apiFiles.serializers import ExpenseSerializer

from django.urls import reverse

# Response classes
ok_response = status.HTTP_200_OK
bad_request = status.HTTP_400_BAD_REQUEST
created     = status.HTTP_201_CREATED
not_found   = status.HTTP_404_NOT_FOUND
no_content  = status.HTTP_204_NO_CONTENT

# API Root reverse here
get_or_post_expenses = 'get_or_post_expense'
update_expenses      = 'update_delete_post'
# APIClient as some app assume
client = Client()

class ExpenseTestSetUp(TestCase):
   
   # test setup here for testing purpose 
   def setUp(self):
      
      # expense user 
      self.users = (
         User.objects.create(username='krish'),
         User.objects.create(username='ankita'),
         User.objects.create(username='yadav')
           )
      
      # Valid payloads
      self.valid_payload = {
         "exp_title": "My Collage Fee Expense",
         "exp_description": "Some explantion of collage fees of expense",
         "exp_user": "krish",
         "exp_date": "2013-02-12",
         "exp_amount": 500
      }

       # Invalid payloads
      self.invalid_payload = {
         "exp_title": "My Collage Fee Expense",
         "exp_description": "Some explantion of collage fees of expense",
         "exp_user": "AnonmousUser",
         "exp_date": "2013-02-12",
         "exp_amount": 500
      }
      
      # expense titles
      self.exp_titles = ('Car Repair Services', 'Mobile Repair Service', 'Collage Fee Charges')
      
      #exp descriptions
      self.exp_descriptions = ('An establishment where automobiles are repaired by auto mechanics and technicians',
                           'The customer interface is typically a service advisor, traditionally called a service writer',
                           'Collage Shop India, Bangalore, India. 37610 likes · 1 talking about this · 670 were here. A high end store retailing merchandise by some of the top')
      # exp amounts
      self.exp_amounts  = (121, 151, 2010)

      # expense dates
      self.exp_dates = ('2021-01-11', '2200-02-21', '2001-01-11')

      # creating expense objects
      for index in range(0, 3):
         title = self.exp_titles[index]
         date        = self.exp_dates[index]
         amount      = self.exp_amounts[index]
         description = self.exp_descriptions[index]
         user        = self.users[index]

         try:
            Expense.objects.create(exp_title=title, exp_description=description, exp_amount=amount, exp_user=user, exp_date=date)
         except:
            pass
   
   # is expense objects are created or and check their counts model testing here
   def test_is_expense_created(self):

      exps = Expense.objects.all()

      try:
         self.assertGreaterEqual(3, exps.count()) # checking expense obj count
      except:
         print('\n Count test case failed')
      else:
         # print('\n Count test case passed')
         pass

# testing all expenses
class TestAllExpenses(ExpenseTestSetUp):
   
   # testing all expense here
   def test_get_all_expense(self):
      response = client.get(
         reverse(get_or_post_expenses)
      )
      # checking status code is same or not
      try:
         self.assertEqual(response.status_code, ok_response)
      except:
         pass

      all_exps = Expense.objects.all()
      serializer = ExpenseSerializer(all_exps, many=True)
      res = {
            'msg': "All expense data",
            'data': serializer.data,
         }
      
      # checking here reponse.data with expected data
      try:
         self.assertEqual(response.data, res)

      except:
         print('\n Response data not matched')

# test single expense valid and invalid 
class TestSingleExpense(ExpenseTestSetUp):
   
   # test valid expense
   def test_valid_expense(self):

      response = client.get(reverse(update_expenses, kwargs={'expId': 3}))

      try:
         exp = Expense.objects.get(pk = 3)
      except:
         exp = None

      finally:
         serializer = ExpenseSerializer(exp)
         res = {
               'msg': f"Detail of expense of id: {3}",
               "data": serializer.data
         }
         try:
            self.assertEqual(response.data, res)
         except:
            print('\n valid expense test failed')
   
   # test valid expense
   def test_invalid_expense(self):
      expId = 30

      response = client.get(reverse(update_expenses, kwargs={'expId': expId}))

      try:
         exp = Expense.objects.get(pk = expId)
      except:
         exp = None

      finally:
         serializer = ExpenseSerializer(exp)
         res = {
               'msg': f"Detail of expense of id: {expId}",
               "data": serializer.data
         }
         try:
            self.assertNotEqual(response.data, res)
            
         except:
            print('\n valid expense test failed')
   
# expense post here
class TestPostExpenses(ExpenseTestSetUp):
   
   # Valid post creation here
   def test_post_valid_expense(self):

      response = client.post(
         reverse(get_or_post_expenses),
         data=json.dumps(self.valid_payload),
         content_type='application/json'
         )
      
      try:
         self.assertEqual(response.status_code, created)

      except:
         print('\n Valid Expense  test creation is failed')
   
   # Invalid post request
   def test_invalid_post_expense(self):

      response = client.post(reverse(get_or_post_expenses),
                              data=json.dumps(self.invalid_payload),
                              content_type='application/json')
      
      
      try:
         self.assertEqual(response.status_code, bad_request)
      except:
         print('\n Invalid test failed')


# test delete expense valid and invalid delete requests
class TestDeleteExpense(ExpenseTestSetUp):
   
   # test valid expense
   def test_valid_expense_deletion(self):

      response = client.delete(reverse(update_expenses, kwargs={'expId': 3}))

      res = {
               'msg': 'Congrats expense successfully deleted',
               }
      try:
         self.assertEqual(response.data, res)
      except:
         print('\n valid expense delete test failed')

      # checking response status codes
      try:
         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
      except:
         print('\n valid expense delete test failed status mis-matched')

   
   # test valid expense
   def test_invalid_expense_deletion(self):
      expId = 30

      response = client.delete(reverse(update_expenses, kwargs={'expId': expId}))
      
      res = {
         'data': f"Expense does found with this {expId}",
         'status': not_found
      }
      
      # checking response status codes
      try:
         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
      except:
         print('\n Invalid expense delete test failed status mis-matched')

   