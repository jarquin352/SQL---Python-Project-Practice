Alter code needed to add constraINTS TO blurt_analysis

ALTER TABLE project1.blurt_analysis ADD CONSTRAINT confid_check CHECK((confidence >= 0) AND (confidence <= 10));
ALTER TABLE project1.blurt_analysis ADD CONSTRAINT sent_check CHECK((sentiment >= -5) AND (sentiment <= 5));SELECT `blurt_analysis`.`email`,
______________________________________________________________________________________________________________
PROBLEM 1_____________________________________________________________________
SELECT user.name, user.address
FROM project1.user
WHERE YEAR(user.date_of_birth) >= 1970 AND YEAR(user.date_of_birth) < 1990
ORDER BY date_of_birth

PROBLEM 2______________________________________________________________________
SELECT vendor.name, advertisement.content 
FROM project1.advertisement, project1.vendor
WHERE advertisement.vendorid = vendor.id

PROBLEM 3______________________________________________________________________
ALL users, with dups
SELECT DISTINCT user.name, user.address
FROM project1.user JOIN project1.hobby 
ON (user.email = hobby.email)
WHERE (hobby = 'swimming' OR hobby = 'dancing')

check solution 
SELECT user.name, user.address, hobby.hobby
FROM project1.user JOIN project1.hobby 
ON (user.email = hobby.email)
WHERE (hobby = 'swimming' OR hobby = 'dancing')

Final Answer, dups dropped addresses ONLY per problem
SELECT DISTINCT user.address
FROM project1.user JOIN project1.hobby 
ON (user.email = hobby.email)
WHERE (hobby = 'swimming' OR hobby = 'dancing')
ORDER BY hobby.hobby

PROBLEM 4_____________________________________________________________________
SELECT b.text, ba.confidence
FROM project1.blurt as b, project1.blurt_analysis as ba
WHERE (b.text REGEXP '^I am reaching') AND (b.blurtid = ba.blurtid)

PROBLEM 5_____________________________________________________________________
SELECT va.email, t.description
FROM project1.vendor_ambassador AS va, project1.topic AS t, project1.vendor_topics AS vt
WHERE (va.vendorid = vt.vendorid) AND (vt.topicid = t.id)

PROBLEM 6_____________________________________________________________________
SELECT ba.email, min(sentiment) AS minSentiment, max(sentiment) AS maxSentiment, avg(confidence) AS avgConfidence
FROM project1.blurt_analysis AS ba
GROUP BY email
ORDER BY `avgConfidence` DESC

PROBLEM 7_____________________________________________________________________
SELECT user.name ,celebrity.email, res.password, res.date_of_birth, celebrity.kind

FROM (
SELECT DISTINCT user.email, user.password, user.date_of_birth
FROM project1.user, project1.celebrity
WHERE user.email NOT IN (SELECT follower FROM project1.follow)) AS res, project1.celebrity, project1.user

WHERE res.email = celebrity.email AND 
	  celebrity.kind = 'MovieStar' AND
      celebrity.email = user.email


PROBLEM 8_____________________________________________________________________
SELECT DISTINCT u1.name AS A, u2.name AS B
FROM project1.user AS u1, project1.user AS u2, project1.blurt_analysis AS ba1, project1.blurt_analysis AS ba2, project1.topic
WHERE u1.email = ba1.email AND
	  u2.email = ba2.email AND
      ba1.topicid = ba2.topicid AND
      (u1.email, u2.email) NOT IN 
      (SELECT * FROM project1.follow) 
      AND u1.email != u2.email

 PROBLEM 9_____________________________________________________________________
SELECT user.name, res.email, res.FollowerCount
FROM project1.user, (
SELECT va.email, count(1) AS FollowerCount
FROM project1.vendor  AS v, project1.vendor_ambassador AS va, project1.follow
WHERE v.id = va.vendorid AND follow.followee = va.email
GROUP BY va.email) as res
WHERE res.email = user.email