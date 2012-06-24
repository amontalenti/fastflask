from nose.tools import (assert_equal, assert_not_equal, assert_true,
                        assert_false, assert_raises, assert_in, assert_is,
                        assert_is_none, assert_is_not, assert_is_not_none,
                        assert_sequence_equal, assert_set_equal,
                        assert_list_equal, assert_dict_equal,
                        assert_items_equal)
from pprint import pprint
from fastco import Article

def test_article_properties():
    article = Article("Is Learning to Code More Popular Than Learning a Foreign Language?",
                      "http://gizmodo.com/5897020/",
                      "foo")
    assert_is_none(article.pub_datetime)
    assert_is_none(article.days_old)
    article.pub_date = "5/28/2012"
    check_article_date(article)
    article.pub_date = "May 28 2012"
    check_article_date(article)

def check_article_date(article):
    assert_equal(article.pub_datetime.month, 5)
    assert_equal(article.pub_datetime.day, 28)
    assert_equal(article.pub_datetime.year, 2012)

