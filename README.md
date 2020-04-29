# Python wrapper for Datasmoothie

## Introduction
This is the python wrapper for the Datasmoothie API. Datasmoothie is a platform that helps people with data processing and visualisation of survey data, weighting and recoding to visualising in interactive dashboards.

The Datasmoothie API is organised around REST. The API has resource oriented URLs, accepts form-encoded requests, returns JSON-encoded responses and uses standard HTTP response codes, authentication and verbs.

### Install and import
Install the client library via the command line:

```pip install --upgrade datasmoothie```

We recommend importing datasmoothie and preserving the namespace:

```import datasmoothie```

## Authenticate
The Datasmoothie API uses API keys to authenticate requests. Datasmoothie users each have their own API key automatically associated with them.

Your API key grants you many privileges, make sure to keep it safe! Don’t check it into a code repository or share it with anyone. Each user should have their own API so that permissions can be revoked if necessary.

To use your API key:

```
import datasmoothie
client = datasmoothie.client(api_key = "[your_key]")
```
The client object can then be used to easily interface with the API.

### Example usage

```

datasource = client.get_datasource(id)
datasource.get_sig_diff('overall', 'agecat')

```
The `get_sig_diff` method returns a dataframe, where the indexes are the answer codes in the datafile and the matrix has positive numbers for a column that is significantly higher than another column, and a negative number for a significantly lower number. In the example below, code 2 is higher than code 1 for answer 3.

<table border="1" class="dataframe">  <thead>    <tr>      <th></th>      <th></th>      <th colspan="5" halign="left">agecat</th>    </tr>    <tr>      <th></th>      <th></th>      <th>1</th>      <th>2</th>      <th>3</th>      <th>4</th>      <th>5</th>    </tr>  </thead>  <tbody>    <tr>      <th rowspan="5" valign="top">overall</th>      <th>1</th>      <td>[]</td>      <td>[]</td>      <td>[]</td>      <td>[]</td>      <td>[]</td>    </tr>    <tr>      <th>2</th>      <td>[]</td>      <td>[]</td>      <td>[]</td>      <td>[]</td>      <td>[]</td>    </tr>    <tr>      <th>3</th>      <td>[2]</td>      <td>[-1]</td>      <td>[]</td>      <td>[]</td>      <td>[]</td>    </tr>    <tr>      <th>4</th>      <td>[]</td>      <td>[]</td>      <td>[]</td>      <td>[]</td>      <td>[]</td>    </tr>    <tr>      <th>5</th>      <td>[]</td>      <td>[]</td>      <td>[]</td>      <td>[]</td>      <td>[]</td>    </tr>  </tbody></table>

The API can also generate tables. The below example shows how to get results, combine them into a single dataframe, and include counts, percentages and base numbers. The tabulation can show unweighted and weighted bases and can automatically generate Excel tables with the results. 

```
datasource.get_tables(['overall', 'price'], 
                      ['gender', 'agecat'], 
                      ['cbase', 'counts', 'c%'], 
                      combine=True)
```
<table border="1" class="dataframe">  <thead>    <tr>      <th></th>      <th>Questions</th>      <th colspan="2" halign="left">Gender</th>      <th colspan="5" halign="left">Age category</th>    </tr>    <tr>      <th></th>      <th>Values</th>      <th>Male</th>      <th>Female</th>      <th>18-24</th>      <th>25-34</th>      <th>35-49</th>      <th>50-64</th>      <th>64+</th>    </tr>    <tr>      <th>Questions</th>      <th>Values</th>      <th></th>      <th></th>      <th></th>      <th></th>      <th></th>      <th></th>      <th></th>    </tr>  </thead>  <tbody>    <tr>      <th>Overall satisfaction</th>      <th>All</th>      <td>209</td>      <td>373</td>      <td>46</td>      <td>127</td>      <td>230</td>      <td>147</td>      <td>32</td>    </tr>    <tr>      <th>Price satisfaction</th>      <th>All</th>      <td>209</td>      <td>373</td>      <td>46</td>      <td>127</td>      <td>230</td>      <td>147</td>      <td>32</td>    </tr>    <tr>      <th rowspan="10" valign="top">Overall satisfaction</th>      <th>Strongly Negative</th>      <td>22</td>      <td>44</td>      <td>5</td>      <td>16</td>      <td>26</td>      <td>17</td>      <td>2</td>    </tr>    <tr>      <th>%</th>      <td>10</td>      <td>11</td>      <td>10</td>      <td>12</td>      <td>11</td>      <td>11</td>      <td>6</td>    </tr>    <tr>      <th>Somewhat Negative</th>      <td>51</td>      <td>87</td>      <td>11</td>      <td>32</td>      <td>47</td>      <td>41</td>      <td>7</td>    </tr>    <tr>      <th>%</th>      <td>24</td>      <td>23</td>      <td>23</td>      <td>25</td>      <td>20</td>      <td>27</td>      <td>21</td>    </tr>    <tr>      <th>Neutral</th>      <td>50</td>      <td>93</td>      <td>16</td>      <td>25</td>      <td>61</td>      <td>33</td>      <td>8</td>    </tr>    <tr>      <th>%</th>      <td>23</td>      <td>24</td>      <td>34</td>      <td>19</td>      <td>26</td>      <td>22</td>      <td>25</td>    </tr>    <tr>      <th>Somewhat Positive</th>      <td>56</td>      <td>92</td>      <td>9</td>      <td>31</td>      <td>59</td>      <td>40</td>      <td>9</td>    </tr>    <tr>      <th>%</th>      <td>26</td>      <td>24</td>      <td>19</td>      <td>24</td>      <td>25</td>      <td>27</td>      <td>28</td>    </tr>    <tr>      <th>Strongly Positive</th>      <td>30</td>      <td>57</td>      <td>5</td>      <td>23</td>      <td>37</td>      <td>16</td>      <td>6</td>    </tr>    <tr>      <th>%</th>      <td>14</td>      <td>15</td>      <td>10</td>      <td>18</td>      <td>16</td>      <td>10</td>      <td>18</td>    </tr>    <tr>      <th rowspan="10" valign="top">Price satisfaction</th>      <th>Strongly Negative</th>      <td>22</td>      <td>50</td>      <td>8</td>      <td>20</td>      <td>22</td>      <td>17</td>      <td>5</td>    </tr>    <tr>      <th>%</th>      <td>10</td>      <td>13</td>      <td>17</td>      <td>15</td>      <td>9</td>      <td>11</td>      <td>15</td>    </tr>    <tr>      <th>Somewhat Negative</th>      <td>47</td>      <td>88</td>      <td>10</td>      <td>30</td>      <td>52</td>      <td>38</td>      <td>5</td>    </tr>    <tr>      <th>%</th>      <td>22</td>      <td>23</td>      <td>21</td>      <td>23</td>      <td>22</td>      <td>25</td>      <td>15</td>    </tr>    <tr>      <th>Neutral</th>      <td>48</td>      <td>92</td>      <td>9</td>      <td>32</td>      <td>59</td>      <td>36</td>      <td>4</td>    </tr>    <tr>      <th>%</th>      <td>23</td>      <td>24</td>      <td>19</td>      <td>25</td>      <td>25</td>      <td>24</td>      <td>12</td>    </tr>    <tr>      <th>Somewhat Positive</th>      <td>58</td>      <td>87</td>      <td>12</td>      <td>25</td>      <td>63</td>      <td>33</td>      <td>12</td>    </tr>    <tr>      <th>%</th>      <td>27</td>      <td>23</td>      <td>26</td>      <td>19</td>      <td>27</td>      <td>22</td>      <td>37</td>    </tr>    <tr>      <th>Strongly Positive</th>      <td>34</td>      <td>56</td>      <td>7</td>      <td>20</td>      <td>34</td>      <td>23</td>      <td>6</td>    </tr>    <tr>      <th>%</th>      <td>16</td>      <td>15</td>      <td>15</td>      <td>15</td>      <td>14</td>      <td>15</td>      <td>18</td>    </tr>  </tbody></table>
