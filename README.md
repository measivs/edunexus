# **EduNexus - Course Management System**

## **Introduction**
This repository contains the Course Management System built with Django REST Framework (DRF). It includes functionalities for user authentication, course and category management, orders, reviews, and permissions. This system was designed with modularity in mind, ensuring a highly adaptable and maintainable structure.

---

## **Features**

### **Users App**
- User Authentication (Signup, Login, Email Verification, etc.).
- Password Reset and Update Mechanism.
- Integration with Email Services for User Notification.

### **Courses App**
- Manage and filter courses based on categories, tags, instructors, and user ratings.
- Implementation of dynamic filters and pagination.
- Optimized course caching for better performance.

### **Categories App**
- CRUD operations to manage hierarchical categories.
- Retrieve all courses related to a specific category.

### **Orders App**
- Place orders for purchasing courses with optional coupons.
- Calculate final prices with applied discounts and taxes.
- Automated user enrollment post-purchase via Django signals.

### **Reviews App**
- Provide user reviews and ratings for courses.
- Implements additional custom permissions for moderators and review creators.

---

# **Endpoints**

## **Categories**

### **List Categories**
- **URL**: `GET /categories/`
- **Functionality**: Retrieve a list of categories.

### **Create Category**
- **URL**: `POST /categories/`
- **Functionality**: Create a new category.

### **Read Category**
- **URL**: `GET /categories/{id}/`
- **Functionality**: Retrieve details of a specific category by its ID.

### **Update Category**
- **URL**: `PUT /categories/{id}/`
- **Functionality**: Fully update an existing category.

### **Partial Update Category**
- **URL**: `PATCH /categories/{id}/`
- **Functionality**: Partially update an existing category.

### **Delete Category**
- **URL**: `DELETE /categories/{id}/`
- **Functionality**: Delete an existing category.

### **List Category Courses**
- **URL**: `GET /categories/{id}/courses/`
- **Functionality**: List courses related to a specific category.

---

## **Coupons**

### **List Coupons**
- **URL**: `GET /coupons/`
- **Functionality**: Retrieve a list of coupons.

### **Create Coupon**
- **URL**: `POST /coupons/`
- **Functionality**: Create a new coupon.

### **Read Coupon**
- **URL**: `GET /coupons/{id}/`
- **Functionality**: Retrieve details of a specific coupon by its ID.

### **Update Coupon**
- **URL**: `PUT /coupons/{id}/`
- **Functionality**: Fully update an existing coupon.

### **Partial Update Coupon**
- **URL**: `PATCH /coupons/{id}/`
- **Functionality**: Partially update an existing coupon.

### **Delete Coupon**
- **URL**: `DELETE /coupons/{id}/`
- **Functionality**: Delete an existing coupon.

---

## **Courses**

### **List Courses**
- **URL**: `GET /courses/`
- **Functionality**: Retrieve a list of courses.

### **Create Course**
- **URL**: `POST /courses/`
- **Functionality**: Create a new course.

### **List Enrollments**
- **URL**: `GET /courses/list_enrollments/`
- **Functionality**: Retrieve a list of course enrollments.

### **List Popular Courses**
- **URL**: `GET /courses/popular-courses/`
- **Functionality**: List popular courses.

### **List Lessons of a Course**
- **URL**: `GET /courses/{course_pk}/lessons/`
- **Functionality**: Retrieve lessons of a specific course.

### **Create Lesson for a Course**
- **URL**: `POST /courses/{course_pk}/lessons/`
- **Functionality**: Create a new lesson for a specific course.

### **Read Lesson**
- **URL**: `GET /courses/{course_pk}/lessons/{id}/`
- **Functionality**: Retrieve a specific lesson by its ID.

### **Update Lesson**
- **URL**: `PUT /courses/{course_pk}/lessons/{id}/`
- **Functionality**: Fully update a specific lesson.

### **Partial Update Lesson**
- **URL**: `PATCH /courses/{course_pk}/lessons/{id}/`
- **Functionality**: Partially update a specific lesson.

### **Delete Lesson**
- **URL**: `DELETE /courses/{course_pk}/lessons/{id}/`
- **Functionality**: Delete a specific lesson.

### **List Reviews of a Course**
- **URL**: `GET /courses/{course_pk}/reviews/`
- **Functionality**: Retrieve reviews for a specific course.

### **Create Review for a Course**
- **URL**: `POST /courses/{course_pk}/reviews/`
- **Functionality**: Create a review for a specific course.

### **Read Review**
- **URL**: `GET /courses/{course_pk}/reviews/{id}/`
- **Functionality**: Retrieve a specific review by its ID.

### **Update Review**
- **URL**: `PUT /courses/{course_pk}/reviews/{id}/`
- **Functionality**: Fully update a specific review.

### **Partial Update Review**
- **URL**: `PATCH /courses/{course_pk}/reviews/{id}/`
- **Functionality**: Partially update a specific review.

### **Delete Review**
- **URL**: `DELETE /courses/{course_pk}/reviews/{id}/`
- **Functionality**: Delete a specific review.

### **Read Course**
- **URL**: `GET /courses/{id}/`
- **Functionality**: Retrieve details of a specific course.

### **Update Course**
- **URL**: `PUT /courses/{id}/`
- **Functionality**: Fully update a specific course.

### **Partial Update Course**
- **URL**: `PATCH /courses/{id}/`
- **Functionality**: Partially update a specific course.

### **Delete Course**
- **URL**: `DELETE /courses/{id}/`
- **Functionality**: Delete a specific course.

### **Retrieve Enrollment for a Course**
- **URL**: `GET /courses/{id}/retrieve_enrollment/`
- **Functionality**: Retrieve enrollment details for a specific course.

---

## **Orders**

### **List Orders**
- **URL**: `GET /orders/`
- **Functionality**: Retrieve a list of orders.

### **Create Order**
- **URL**: `POST /orders/`
- **Functionality**: Create a new order.

### **Read Order**
- **URL**: `GET /orders/{id}/`
- **Functionality**: Retrieve details of a specific order.

### **Update Order**
- **URL**: `PUT /orders/{id}/`
- **Functionality**: Fully update a specific order.

### **Partial Update Order**
- **URL**: `PATCH /orders/{id}/`
- **Functionality**: Partially update a specific order.

### **Delete Order**
- **URL**: `DELETE /orders/{id}/`
- **Functionality**: Delete a specific order.

---

## **Users**

### **List User Balance**
- **URL**: `GET /users/balance/`
- **Functionality**: Retrieve the balance of the user.

### **Add to User Balance**
- **URL**: `POST /users/balance/add/`
- **Functionality**: Add balance to the user's account.

### **User Login**
- **URL**: `POST /users/login/`
- **Functionality**: Log in a user.

### **Request Password Reset**
- **URL**: `POST /users/password_reset/`
- **Functionality**: Request a password reset email.

### **Confirm Password Reset**
- **URL**: `POST /users/password_reset/confirm/`
- **Functionality**: Confirm a password reset.

### **Retrieve User Profile**
- **URL**: `GET /users/profile/`
- **Functionality**: Retrieve the user's profile.

### **Update User Profile**
- **URL**: `PUT /users/profile/`
- **Functionality**: Fully update the user's profile.

### **Partial Update User Profile**
- **URL**: `PATCH /users/profile/`
- **Functionality**: Partially update the user's profile.

### **Register User**
- **URL**: `POST /users/register/`
- **Functionality**: Register a new user.

### **Verify Email**
- **URL**: `POST /users/verify/`
- **Functionality**: Verify the user's email with a 6-digit code.
---

## **Structure**

### **Users App**
| **File Name**           | **Description**                                                      |
|-------------------------|----------------------------------------------------------------------|
| `views.py`              | Provides user-related endpoints for managing authentication, email verification, and password reset. |
| `serializers.py`        | Serializers to manage user entities like profiles, tokens, and verification. |
| `signals.py`            | Contains custom signals to handle user-related events like email verification. |
| `verification.py`       | Contains utility functions to handle email verification codes.      |
| `email.py`              | Handles email functionalities like sending verification and password reset emails. |
| `models.py`             | Defines user-related database models like `User`, `Tokens`, and `Profile`. |
| `urls.py`               | API routes for user-related functionalities.                        |

---

### **Courses App**
| **File Name**           | **Description**                                                      |
|-------------------------|----------------------------------------------------------------------|
| `views.py`              | Manages endpoints for listing, filtering, creating, and retrieving courses. |
| `serializers.py`        | Serializers for course-related entities like `Course` and `Tags`.    |
| `permissions.py`        | Defines custom permissions like `IsInstructor` and `IsCourseOwner`. |
| `models.py`             | Defines database models like `Course` and `Enrollment`.             |
| `filters.py`            | Implements course filtering by tags, ratings, or categories.        |
| `urls.py`               | API routes for course-related operations.                           |

---

### **Categories App**
| **File Name**           | **Description**                                                      |
|-------------------------|----------------------------------------------------------------------|
| `views.py`              | Manage hierarchical categories and fetch courses within categories. |
| `serializers.py`        | Serializers to handle category entities with hierarchical structures.|
| `models.py`             | Defines category-related database models.                           |
| `urls.py`               | Router for category views.                                          |

---

### **Orders App**
| **File Name**           | **Description**                                                      |
|-------------------------|----------------------------------------------------------------------|
| `views.py`              | Manages order placement and retrieval.                              |
| `tasks.py`              | Background tasks for sending emails and processing order information.|
| `signals.py`            | Automatically enroll users in courses after successful purchase.    |
| `serializers.py`        | Serializes orders, including tax calculation and discount application. |
| `permissions.py`        | Custom permissions for handling order creation and management.       |
| `models.py`             | Defines database models for orders and coupons.                     |
| `order_service.py`      | Business logic for handling orders (e.g., price calculation, validations). |
| `order_calculation.py`  | Utility for calculating course prices with discounts and taxes.      |
| `urls.py`               | API routes for order-related functionalities.                       |

---

### **Reviews App**
| **File Name**           | **Description**                                                      |
|-------------------------|----------------------------------------------------------------------|
| `views.py`              | Implementation of review retrieval and creation for courses.         |
| `serializers.py`        | Serializes review input, including user feedback and ratings.        |
| `permissions.py`        | Custom permissions to allow review updates only to the original creator. |
| `models.py`             | Defines review-related models.                                       |

---

## **Installation**

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/measivs/edunexus
   cd edunexus
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run Database Migrations**:
   ```bash
   python manage.py migrate
   ```

4. **Start the Development Server**:
   ```bash
   python manage.py runserver
   ```

---

## **Caching and Background Processing**

### Caching
- Course and enrollment queries are cached with Redis, improving response time.

### Background Tasks
- Uses Celery for background tasks like sending order confirmation emails and about expiring coupons.